import logging
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core import VectorStoreIndex

from src.query import get_query_engine, setup_llm

logger = logging.getLogger(__name__)

def create_rag_agent(index: VectorStoreIndex) -> ReActAgent:
    """
    Creates a ReActAgent with access to the VectorStore RAG query engine as a tool.
    """
    setup_llm()
    
    # Get the standard query engine
    query_engine = get_query_engine(index)
    
    # Define a tool for the agent
    query_tool = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="document_db_tool",
            description="Nützlich, um spezifische Fragen zu Finanzberichten, Bilanzen, Glossaren und Unternehmensdaten zu beantworten."
        )
    )
    
    # Create the ReAct agent
    agent = ReActAgent.from_tools(
        tools=[query_tool],
        verbose=True
    )
    
    return agent
