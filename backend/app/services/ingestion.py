# services/ingestion.py
import hashlib
from pathlib import Path
from backend.app.services.vector_store import VectorStore
from backend.app.services import loader, chunker
from backend.app.services.embedder import get_embeddings
from backend.exception import IngestionError

def file_hash(path: Path) -> str:
    # Hash the file bytes (sha256). This identifies "the same document"
    # even if the filename changes.
    with open(path, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")
    return digest.hexdigest()
    

def ingest(path: str,store: VectorStore) -> dict:
    file_path = Path(path)
    # 1. Validate: does the file exist? Is the extension .pdf or .docx?
    #    Raise a clear error otherwise.
    if not file_path.is_file():
        raise FileNotFoundError(f"Folder does not exist: {file_path}")

    if file_path.suffix.lower() not in {".pdf",".docx"}:
        raise ValueError(f"unsupported filr type'{file_path.suffix}'. expected .pdf")

    # 2. Idempotency check: compute the hash and ask the vector store
    #    whether this doc_id already exists. If yes, skip and return early.
    
    doc_id = file_hash(path)   # computed once per file, before chunking
    if store.has_document(doc_id=doc_id):
        return {"doc_id": doc_id, "filename":file_path.name,
                "chunks_added":0,"skipped": True}

    # 3. Load: use your PDF/DOCX loader to get pages or sections of text

    pages = loader.load_document(local_path=str(file_path),source=file_path.name)
    if not pages:
        raise FileNotFoundError(f"loader failed to load file from path in ingestion: {file_path}")
    # 4. Chunk: split with your splitter (size, overlap)

    chunks = chunker.convertTochunks(pages)
    if not chunks:
        print("error occured at ingestion while chunking")
        raise IngestionError("no chunks produced in ingestion")

    # 5. Attach metadata to every chunk:
    #    doc_id, source (filename), page, chunk_index
    #    Build a deterministic chunk id: f"{doc_id}-{chunk_index}"

    #  3 parallel list help to get the ids and metadata in order if any things less in no. this mismatch happen
    texts, metadatas, ids = [], [], []
    for i, chunk in enumerate(chunks):
        chunk.metadata['doc_id'] = doc_id
        chunk.metadata['source'] = file_path.name
        chunk.metadata['chunk_index'] = i

        texts.append(chunk.page_content)
        metadatas.append(chunk.metadata)
        ids.append(f"{doc_id}-{i}")
    # 6. Embed + store: add chunks to the vector store using those ids

    VectorStore.add(texts=texts,metadatas=metadatas,ids=ids)

    # 7. Return a summary
    return {"doc_id": doc_id, "filename": path.name, "chunks_added": texts[0][:10]}