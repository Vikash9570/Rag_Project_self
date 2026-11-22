"""Thin wrapper around Chroma: add chunks, search top-k, reset the index."""

import chromadb
from pathlib import Path
from functools import lru_cache
from backend.app.config import settings
from backend.app.services.embedder import get_embeddings 


class VectorStore():
    def __init__(self,Embd_obj, persist_dir,name):
        self._embd_fn = Embd_obj
        self._client = chromadb.PersistentClient(path=str(persist_dir))
        self.coll_name = name
        self._col = self._make_collection()


    def _make_collection(self):
        # cosine distance: 0 = identical, larger = less similar
        try:    
            return self._client.get_or_create_collection(
                self.coll_name, metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"error occured at vector_store/make_collection {e}")
            raise

    def add(self, texts: list[str], metadatas: list[dict], ids) -> None:
        try:
            if not texts:
                return
            # Chroma rejects None metadata values, so drop them (e.g. page=None for .txt)
            clean = [{k: v for k, v in m.items() if v is not None} for m in metadatas]
            self._col.upsert(
                ids=ids, documents=texts, embeddings=self._embd_fn.embed_documents(texts), metadatas=clean
            )
        except Exception as e:
            print(f"error occured at add func in vector store while adding id: {e}")
            raise

    def search(self, query: str, k: int = 4) -> list[dict]:
        n = self._col.count()
        if n == 0:
            return []
        res = self._col.query(
            query_embeddings=self._embd_fn.embed_query(query), n_results=min(k, n)
        )
        return [
            {"text": t, "metadata": m, "distance": d, "source": m.get("source")}
            for t, m, d in zip(
                res["documents"][0], res["metadatas"][0], res["distances"][0]
            )
        ]

    def has_document(self,doc_id: str)->bool:
        res = self._col.get(where={"doc_id":doc_id},limit=1,include=[])
        return len(res['ids'])>0

    def count(self) -> int:
        return self._col.count()

    def reset(self) -> None:
        self._client.delete_collection(self.coll_name)
        self._coll = self._make_collection()

     
@lru_cache(maxsize=1)
def get_store()->VectorStore:
    return VectorStore(get_embeddings(),settings.vector_db_dir,settings.collection_name)