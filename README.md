# RAG

A local RAG (Retrieval-Augmented Generation) CLI for querying financial and annual-report PDFs. Docling parses PDFs to Markdown, LlamaIndex chunks and indexes them into a persistent ChromaDB store, and a local Ollama LLM answers questions. Runs fully locally — no API keys required.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install [Ollama](https://ollama.com) and pull the model:
   ```bash
   ollama pull llama3.2
   ```
3. Add your PDFs to `data/pdfs/`.

## Usage

Run from the repo root:

```bash
python main.py
```

Menu options:

| Option | Description |
|---|---|
| `ingest` | Parses, chunks, and indexes all PDFs in `data/pdfs/`. Idempotent — safe to re-run; unchanged documents are skipped, changed ones are re-indexed. |
| `query` | Ask a free-text question, answered from the top matching chunks. |
| `structured` | Extract structured financial data (company, KPIs, risks, summary) from a named document as a Pydantic object. |
| `agent` | Interactive ReAct agent with access to the document index as a tool. |
| `exit` | Quit. |

## Configuration

Settings live in `config.py` — LLM provider/model, Ollama URL, embedding model, and Chroma collection name.

## Notes

- `data/`, `parsed/`, and `embeddings/` are gitignored — a fresh clone starts empty; add PDFs and run `ingest` first.
- See `CLAUDE.md` for architecture details.
