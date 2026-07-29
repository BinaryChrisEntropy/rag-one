from pathlib import Path
from typing import List
from llama_index.core import Document
from llama_index.core.schema import BaseNode
from llama_index.core.node_parser import MarkdownNodeParser

def chunk_markdown_file(markdown_path: Path) -> List[BaseNode]:
    """
    Reads a Markdown file, loads it into a LlamaIndex Document,
    and parses it into nodes based on Markdown headers.
    """
    markdown_path = Path(markdown_path)
    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Create a document and attach metadata
    document = Document(
        text=content,
        metadata={
            "file_name": markdown_path.name,
            "source_pdf": f"{markdown_path.stem}.pdf"
        }
    )

    # Use MarkdownNodeParser to chunk by headers
    parser = MarkdownNodeParser()
    nodes = parser.get_nodes_from_documents([document])
    
    return nodes
