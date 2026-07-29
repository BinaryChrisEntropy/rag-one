import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
PARSED_DIR = BASE_DIR / "parsed"
EMBEDDINGS_DIR = BASE_DIR / "embeddings"

# Ensure directories exist
for directory in [DATA_DIR, PDF_DIR, PARSED_DIR, EMBEDDINGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# LLM and Embedding Config
LLM_PROVIDER = "ollama"  # or "openai", etc.
OLLAMA_MODEL = "llama3.2"
OLLAMA_BASE_URL = "http://localhost:11434"

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# ChromaDB Config
CHROMA_COLLECTION_NAME = "rag_docling_collection"
