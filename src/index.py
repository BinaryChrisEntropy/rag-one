import chromadb
from pathlib import Path
from typing import List
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.schema import BaseNode

from config import EMBEDDINGS_DIR, CHROMA_COLLECTION_NAME, EMBEDDING_MODEL_NAME

def setup_global_settings():
    """
    Configures global LlamaIndex settings such as the embedding model.
    """
    # Configure the embedding model globally
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL_NAME)

def get_or_create_index(nodes: List[BaseNode] = None) -> VectorStoreIndex:
    """
    Sets up ChromaDB vector store and creates or loads the VectorStoreIndex.
    If nodes are provided and index is empty, it populates it.
    """
    setup_global_settings()
    
    # Initialize Persistent ChromaDB Client
    db = chromadb.PersistentClient(path=str(EMBEDDINGS_DIR))
    
    # Get or create collection
    chroma_collection = db.get_or_create_collection(CHROMA_COLLECTION_NAME)
    
    # Create Chroma Vector Store
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # Create Storage Context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    if nodes:
        # Build index from nodes (this will create embeddings)
        index = VectorStoreIndex(nodes, storage_context=storage_context)
        return index
    else:
        # Load index from the existing vector store
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            storage_context=storage_context
        )
        return index
