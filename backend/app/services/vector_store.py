"""Thin wrapper around Chroma: add chunks, search top-k, reset the index."""

from langchain_core.vectorstores import VectorStore
import chromadb
from backend.app.services.embedder import get_embeddings
from backend.app.config import settings
from pathlib import Path
import hashlib
from ingestion import file_hash


class VectorStore():
    def __init__(self,Embd_fn, persist_dir,name):
        self._embd_fn = Embd_fn
        self._client = chromadb.PersistentClient(path=str(persist_dir))
        self.coll_name = name
        self._col = self._make_collection()

    def _make_collection(self):
        # cosine distance: 0 = identical, larger = less similar
        return self._client.get_or_create_collection(
            self._name, metadata={"hnsw:space": "cosine"}
        )

    def add(self, texts: list[str], metadatas: list[dict]) -> None:
        try:
            if not texts:
                return
            # Chroma rejects None metadata values, so drop them (e.g. page=None for .txt)
            clean = [{k: v for k, v in m.items() if v is not None} for m in metadatas]
            # Deterministic IDs: adding the same chunk twice replaces it instead of duplicating
            ids = [
                hashlib.sha1(f"{m.get('source', '')}|{t}".encode()).hexdigest()
                for t, m in zip(texts, clean)
            ]
            self._col.upsert(
                ids=ids, documents=texts, embeddings=self._embed(texts), metadatas=clean
            )
        except Exception as e:
            print(f"error occured at add func in vector store while adding id: {e}")

    def search(self, query: str, k: int = 4) -> list[dict]:
        n = self._col.count()
        if n == 0:
            return []
        res = self._col.query(
            query_embeddings=self._embed([query]), n_results=min(k, n)
        )
        return [
            {"text": t, "metadata": m, "distance": d}
            for t, m, d in zip(
                res["documents"][0], res["metadatas"][0], res["distances"][0]
            )
        ]

    def count(self) -> int:
        return self._col.count()

    def reset(self) -> None:
        self._client.delete_collection(self._name)
        self._col = self._make_collection()

     
