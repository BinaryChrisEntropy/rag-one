import logging
from pathlib import Path
from docling.document_converter import DocumentConverter
from config import PARSED_DIR

logger = logging.getLogger(__name__)

def parse_pdf_to_markdown(pdf_path: Path, force_reparse: bool = False) -> Path:
    """
    Parses a PDF file using Docling, extracts content as Markdown, and saves it.
    If the file has already been parsed, it reads from cache unless force_reparse is True.
    """
    pdf_path = Path(pdf_path)
    output_filename = f"{pdf_path.stem}.md"
    output_path = PARSED_DIR / output_filename

    if output_path.exists() and not force_reparse:
        logger.info(f"Using cached parsed document: {output_path}")
        return output_path

    logger.info(f"Parsing PDF with Docling: {pdf_path}")
    converter = DocumentConverter()
    
    # Run the conversion
    result = converter.convert(pdf_path)
    
    # Export to markdown format (retains tables, headings, paragraphs)
    markdown_content = result.document.export_to_markdown()
    
    # Save the parsed markdown
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    logger.info(f"Successfully saved parsed Markdown to: {output_path}")
    return output_path
