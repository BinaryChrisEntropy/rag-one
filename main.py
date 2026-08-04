import sys
import logging
from src.ingest import run_ingestion
from src.index import get_or_create_index
from src.query import get_query_engine, get_structured_query_engine
from src.models import BusinessReportSummary
from src.agent import create_rag_agent

# Setup basic logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("main")

def print_help():
    print("""
Options:
  1. ingest       - Reads all PDFs in 'data/pdfs/' with Docling, chunks them, and indexes them in ChromaDB.
  2. query        - Asks a direct question against the RAG vector index.
  3. structured   - Extracts structured Pydantic data (BusinessReportSummary) from the document.
  4. agent        - Starts an interactive conversation with the ReAct RAG agent.
  5. exit         - Exits the program.
""")

def handle_query():
    try:
        index = get_or_create_index()
        query_engine = get_query_engine(index)
        while True:
            question = input("\nYour question (or 'back'): ")
            if question.strip().lower() == 'back':
                break
            if not question.strip():
                continue
            print("\nSearching...")
            response = query_engine.query(question)
            print("\nAnswer:")
            print(response)
    except Exception as e:
        print(f"Error: {e}. Have you already run 'ingest'?")

def handle_structured():
    try:
        index = get_or_create_index()
        query_engine = get_structured_query_engine(index, BusinessReportSummary)

        doc_name = input("\nWhich document would you like to analyze in structured form? (e.g. AR2025_Glossary): ").strip()
        if not doc_name:
            print("No document specified.")
            return

        query_str = f"Extract all financial data, KPIs, and summaries for the document {doc_name}."
        print(f"\nExtracting structured data for {doc_name} (this may take a moment)...")

        response = query_engine.query(query_str)

        # response.response is a Pydantic object of class BusinessReportSummary
        structured_data = response.response

        print("\n=== Structured Pydantic Output ===")
        print(f"Company:           {structured_data.company_name}")
        print(f"Report type:       {structured_data.report_type}")
        print(f"Reporting period:  {structured_data.reporting_period}")
        print(f"\nSummary:\n{structured_data.summary}")

        print("\nKey metrics:")
        for metric in structured_data.key_metrics:
            year_str = f" ({metric.year})" if metric.year else ""
            context_str = f" - {metric.context}" if metric.context else ""
            print(f" - {metric.name}: {metric.value}{year_str}{context_str}")

        print("\nRisks / challenges:")
        for risk in structured_data.challenges_or_risks:
            print(f" - {risk}")

    except Exception as e:
        print(f"Error during structured extraction: {e}")

def handle_agent():
    try:
        index = get_or_create_index()
        agent = create_rag_agent(index)
        print("\nAgent is ready. You can ask questions. Type 'back' to return to the main menu.")
        while True:
            question = input("\nAgent question: ")
            if question.strip().lower() == 'back':
                break
            if not question.strip():
                continue
            response = agent.chat(question)
            print("\nAgent answer:")
            print(response)
    except Exception as e:
        print(f"Error starting the agent: {e}")

def main():
    print("=== Welcome to the Docling + LlamaIndex RAG System ===")

    while True:
        print_help()
        choice = input("Choose an option (1-5): ").strip()

        if choice in ['1', 'ingest']:
            print("\nStarting document ingestion...")
            run_ingestion()
        elif choice in ['2', 'query']:
            handle_query()
        elif choice in ['3', 'structured']:
            handle_structured()
        elif choice in ['4', 'agent']:
            handle_agent()
        elif choice in ['5', 'exit']:
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please choose 1-5.")

if __name__ == "__main__":
    main()