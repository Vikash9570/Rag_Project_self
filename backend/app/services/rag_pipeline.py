# services/rag_pipeline.py
from backend.app.services.vector_store import VectorStore
from backend.app.services.generator import get_llm, build_user_message, system_prompt
from langchain_core.messages import HumanMessage,SystemMessage



def ask(question: str, k: int = 4) -> dict:
    # 1. Retrieve: get top-k chunks (with metadata) from your vector store   
    chunks = VectorStore().similarity_search(
        query=question,
        k=k,
    )
    
    # 2. Guard: if nothing relevant came back, return early
    #    (decide: empty list? a similarity score threshold?)
    if not chunks:
        return {"answer": "I couldn't find this in the provided documents.", "sources": []}

    # 3. Build the prompt: reuse build_user_message(chunks, question)
    llm = get_llm()

    prompt = build_user_message(chunks=chunks,question=question)
    # 4. Call the LLM: SystemMessage + HumanMessage via get_llm().invoke(...)
    messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=prompt)]
    
    response = llm.invoke(messages)
    # 5. Return a structured result, not just a string

    return {
        "answer": response,
        "sources": [response],   # source file, page, chunk id
    }


    