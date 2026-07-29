import logging
from typing import Type
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama

from config import OLLAMA_MODEL, OLLAMA_BASE_URL, LLM_PROVIDER
from src.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def setup_llm():
    """
    Sets up the global LLM Settings based on the configuration.
    """
    if LLM_PROVIDER == "ollama":
        # Configure Ollama LLM
        Settings.llm = Ollama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            request_timeout=300.0,
            system_prompt=SYSTEM_PROMPT
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

def get_query_engine(index: VectorStoreIndex):
    """
    Returns a standard text-based RAG query engine.
    """
    setup_llm()
    return index.as_query_engine(similarity_top_k=5)

def get_structured_query_engine(index: VectorStoreIndex, response_schema: Type[BaseModel]):
    """
    Returns a RAG query engine that outputs parsed Pydantic objects.
    """
    setup_llm()
    # LlamaIndex query engine automatically supports output_cls for structured outputs!
    return index.as_query_engine(
        similarity_top_k=7,
        output_cls=response_schema
    )
