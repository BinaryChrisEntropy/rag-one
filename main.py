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
Optionen:
  1. ingest       - Liest alle PDFs in 'data/pdfs/' mit Docling, chunked sie und indiziert sie in ChromaDB.
  2. query        - Stellt eine direkte Frage an den RAG Vector Index.
  3. structured   - Extrahiert strukturierte Pydantic-Daten (BusinessReportSummary) aus dem Dokument.
  4. agent        - Startet eine interaktive Konversation mit dem ReAct-RAG-Agenten.
  5. exit         - Beendet das Programm.
""")

def handle_query():
    try:
        index = get_or_create_index()
        query_engine = get_query_engine(index)
        while True:
            question = input("\nIhre Frage (oder 'back'): ")
            if question.strip().lower() == 'back':
                break
            if not question.strip():
                continue
            print("\nSuche läuft...")
            response = query_engine.query(question)
            print("\nAntwort:")
            print(response)
    except Exception as e:
        print(f"Fehler: {e}. Haben Sie bereits 'ingest' ausgeführt?")

def handle_structured():
    try:
        index = get_or_create_index()
        query_engine = get_structured_query_engine(index, BusinessReportSummary)
        
        doc_name = input("\nWelches Dokument möchten Sie strukturiert analysieren? (z.B. AR2025_Glossary): ").strip()
        if not doc_name:
            print("Kein Dokument angegeben.")
            return

        query_str = f"Extrahiere alle Finanzdaten, KPIs und Zusammenfassungen für das Dokument {doc_name}."
        print(f"\nExtrahiere strukturierte Daten für {doc_name} (das kann einen Moment dauern)...")
        
        response = query_engine.query(query_str)
        
        # response.response is a Pydantic object of class BusinessReportSummary
        structured_data = response.response
        
        print("\n=== Strukturierte Pydantic-Ausgabe ===")
        print(f"Unternehmen: {structured_data.company_name}")
        print(f"Berichtstyp: {structured_data.report_type}")
        print(f"Zeitraum:    {structured_data.reporting_period}")
        print(f"\nZusammenfassung:\n{structured_data.summary}")
        
        print("\nKennzahlen:")
        for metric in structured_data.key_metrics:
            year_str = f" ({metric.year})" if metric.year else ""
            context_str = f" - {metric.context}" if metric.context else ""
            print(f" - {metric.name}: {metric.value}{year_str}{context_str}")
            
        print("\nRisiken / Herausforderungen:")
        for risk in structured_data.challenges_or_risks:
            print(f" - {risk}")
            
    except Exception as e:
        print(f"Fehler bei der strukturierten Extraktion: {e}")

def handle_agent():
    try:
        index = get_or_create_index()
        agent = create_rag_agent(index)
        print("\nAgent ist bereit. Sie können Fragen stellen. Geben Sie 'back' ein, um zum Hauptmenü zu gelangen.")
        while True:
            question = input("\nAgent-Frage: ")
            if question.strip().lower() == 'back':
                break
            if not question.strip():
                continue
            response = agent.chat(question)
            print("\nAgent Antwort:")
            print(response)
    except Exception as e:
        print(f"Fehler beim Starten des Agenten: {e}")

def main():
    print("=== Willkommen beim Docling + LlamaIndex RAG System ===")
    
    while True:
        print_help()
        choice = input("Wählen Sie eine Option (1-5): ").strip()
        
        if choice in ['1', 'ingest']:
            print("\nStarte Dokumenten-Ingestion...")
            run_ingestion()
        elif choice in ['2', 'query']:
            handle_query()
        elif choice in ['3', 'structured']:
            handle_structured()
        elif choice in ['4', 'agent']:
            handle_agent()
        elif choice in ['5', 'exit']:
            print("Auf Wiedersehen!")
            sys.exit(0)
        else:
            print("Ungültige Option. Bitte wählen Sie 1-5.")

if __name__ == "__main__":
    main()