import logging
import sys
from pathlib import Path
from config import PDF_DIR
from src.parse import parse_pdf_to_markdown
from src.chunk import chunk_markdown_file
from src.index import (
    get_or_create_index,
    get_indexed_state,
    delete_source_from_index,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ingest")

def run_ingestion(force_reparse: bool = False, force_reindex: bool = False):
    """
    Main ingestion workflow.

    Ingestion is idempotent: a document whose content is already indexed is
    skipped, and a changed document replaces its previous nodes instead of
    being added a second time. Use force_reindex=True to re-embed everything.
    """
    logger.info("Starting ingestion workflow...")
    
    # 1. Find all PDFs and sort by size (ascending)
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    pdf_files.sort(key=lambda p: p.stat().st_size)
    if not pdf_files:
        logger.warning(f"No PDF files found in {PDF_DIR}. Please add some PDFs.")
        return
        
    logger.info(f"Found {len(pdf_files)} PDF(s) to process.")
    
    # 2. Get or create index (empty or loaded)
    index = get_or_create_index()
    
    # 3. Parse, chunk, and index each PDF incrementally
    for pdf_path in pdf_files:
        try:
            logger.info(f"Processing: {pdf_path.name} ({pdf_path.stat().st_size / 1024:.1f} KB)")
            
            # Parse with Docling
            markdown_path = parse_pdf_to_markdown(pdf_path, force_reparse=force_reparse)
            
            # Chunk with MarkdownNodeParser (cheap - no embeddings yet)
            nodes = chunk_markdown_file(markdown_path)
            if not nodes:
                logger.warning(f"No nodes generated for {pdf_path.name}.")
                continue

            # Skip documents that are already indexed exactly once with identical
            # content. A mismatching node count means stale or duplicated entries,
            # which the deletion below cleans up.
            content_hash = nodes[0].metadata["content_hash"]
            indexed_count, indexed_hashes = get_indexed_state(index, pdf_path.name)
            is_current = indexed_hashes == {content_hash} and indexed_count == len(nodes)
            if is_current and not force_reindex:
                logger.info(f"{pdf_path.name} is unchanged and already indexed. Skipping.")
                continue

            # Replace any previous (or duplicated) nodes for this document
            deleted = delete_source_from_index(index, pdf_path.name)
            if deleted:
                logger.info(f"Removed {deleted} outdated node(s) for {pdf_path.name}.")

            logger.info(f"Generated {len(nodes)} nodes. Inserting into index...")
            index.insert_nodes(nodes)
            logger.info(f"Successfully indexed {pdf_path.name}.")
        except Exception as e:
            logger.error(f"Error processing {pdf_path.name}: {e}", exc_info=True)
            
    logger.info("Ingestion completed successfully.")
    return index

if __name__ == "__main__":
    run_ingestion()
