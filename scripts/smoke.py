# scripts/smoke.py
from backend.app.services.vector_store import get_store
from backend.app.services.ingestion import ingest
from backend.app.services.rag_pipeline import ask

PDF = "backend/data/uploads/Abstract.pdf"   # any PDF you have in uploads/

store = get_store()

print("1st ingest:", ingest(PDF, store))     # expect chunks_added > 0, skipped False
print("2nd ingest:", ingest(PDF, store))     # expect chunks_added 0, skipped True
print("store count:", store.count())

result = ask("what are the measures to prevent plants from insects")
print("\nANSWER:", result["answer"])
for s in result["sources"]:
    print("-", s["source"], "page", s["page"], "|", s["text"][:80])



