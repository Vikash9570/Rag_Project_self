# Rag_End_to_End

A simple RAG app: upload a document, ask questions about it, and get answers grounded in the retrieved chunks.

- **Backend:** FastAPI, Chroma (vector store), sentence-transformers (embeddings), Anthropic (generation)
- **Frontend:** a single static HTML file in `frontend/index.html`
- **Tooling:** [uv](https://docs.astral.sh/uv/) for Python and dependencies

## Setup

```bash
uv sync                       # creates .venv and uv.lock from pyproject.toml
cp .env.example .env          # then set ANTHROPIC_API_KEY
```

## Run

```bash
uv run uvicorn app.main:app --reload --app-dir backend
```

Then open `frontend/index.html` in a browser, untick "Demo mode", and keep the API base URL at `http://localhost:8000`.
Check the API is up at <http://localhost:8000/health>.

## API contract

| Method | Path      | Request                         | Response                                                        |
| ------ | --------- | ------------------------------- | --------------------------------------------------------------- |
| POST   | `/upload` | multipart, field `file`         | `{ "message": str, "chunks": int }`                             |
| POST   | `/ask`    | `{ "question": str }`           | `{ "answer": str, "sources": [{ "text", "source", "page" }] }`  |
| GET    | `/health` | none                            | `{ "status": "ok" }`                                            |

`/upload` and `/ask` currently return `501` until the pipeline is implemented.

## Layout

```
backend/app/
  main.py          app, CORS, router registration
  config.py        every tunable value (chunk size, top-k, models, paths)
  schemas.py       request/response models
  api/             thin routes: upload.py, ask.py
  services/        loader, chunker, embedder, vector_store, generator
backend/data/      uploads and the persisted index (gitignored)
backend/tests/
frontend/index.html
```

## Build order

1. `services/loader.py` and `services/chunker.py`, with tests
2. `services/embedder.py` and `services/vector_store.py`
3. `services/generator.py`
4. Wire `/upload` and `/ask`, then turn off demo mode in the frontend
5. Add a small evaluation set of questions with known answers before tuning anything

## Tests

```bash
uv run pytest
```

