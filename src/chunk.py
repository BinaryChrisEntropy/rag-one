import hashlib
from pathlib import Path
from typing import List
from llama_index.core import Document
from llama_index.core.schema import BaseNode
from llama_index.core.node_parser import MarkdownNodeParser

def chunk_markdown_file(markdown_path: Path) -> List[BaseNode]:
    """
    Reads a Markdown file, loads it into a LlamaIndex Document,
    and parses it into nodes based on Markdown headers.

    Every node carries a 'content_hash' of the whole source document and a
    deterministic node id, so that re-ingesting the same document can be
    detected and cannot produce duplicate entries in the vector store.
    """
    markdown_path = Path(markdown_path)
    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()

    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    # Create a document and attach metadata
    document = Document(
        text=content,
        metadata={
            "file_name": markdown_path.name,
            "source_pdf": f"{markdown_path.stem}.pdf",
            "content_hash": content_hash
        },
        # The hash is bookkeeping only - keep it out of embeddings and prompts
        excluded_embed_metadata_keys=["content_hash"],
        excluded_llm_metadata_keys=["content_hash"]
    )

    # Use MarkdownNodeParser to chunk by headers
    parser = MarkdownNodeParser()
    nodes = parser.get_nodes_from_documents([document])

    # Derive stable ids from the content itself instead of random UUIDs
    for position, node in enumerate(nodes):
        chunk_hash = hashlib.sha256(node.get_content().encode("utf-8")).hexdigest()
        node.id_ = f"{markdown_path.stem}-{position:04d}-{chunk_hash[:12]}"

    return nodes
