import logging
import sys
from pathlib import Path
from config import PDF_DIR
from src.parse import parse_pdf_to_markdown
from src.chunk import chunk_markdown_file
from src.index import get_or_create_index

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ingest")

def run_ingestion(force_reparse: bool = False):
    """
    Main ingestion workflow.
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
            
            # Chunk with MarkdownNodeParser
            nodes = chunk_markdown_file(markdown_path)
            if nodes:
                logger.info(f"Generated {len(nodes)} nodes. Inserting into index...")
                index.insert_nodes(nodes)
                logger.info(f"Successfully indexed {pdf_path.name}.")
            else:
                logger.warning(f"No nodes generated for {pdf_path.name}.")
        except Exception as e:
            logger.error(f"Error processing {pdf_path.name}: {e}", exc_info=True)
            
    logger.info("Ingestion completed successfully.")
    return index

if __name__ == "__main__":
    run_ingestion()
