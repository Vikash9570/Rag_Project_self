# services/rag_pipeline.py
from backend.app.services.vector_store import get_store
from backend.app.services import generator
from langchain_core.messages import HumanMessage,SystemMessage



def ask(question: str, k: int = 4) -> dict:
    # 1. Retrieve: get top-k chunks (with metadata) from your vector store   
    chunks = get_store().search(
        query=question,
        k=k,
    )
    
    # 2. Guard: if nothing relevant came back, return early
    #    (decide: empty list? a similarity score threshold?)
    if not chunks:
        return {"answer": "I couldn't find this in the provided documents.", "sources": []}

    # 4. Call the LLM: SystemMessage + HumanMessage via get_llm().invoke(...)
   
    response = generator.answer(chunks,question=question)
    # 5. Return a structured result, not just a string

    return {
        "answer": response,
        "sources": [response],   # source file, page, chunk id
    }


    