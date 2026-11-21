# services/rag_pipeline.py
import chunker,vector_store,generator,loader
from langchain_core.messages import HumanMessage,SystemMessage
from app.schemas import AskResponse


def ask(question: str, k: int = 4) -> dict:
    # 1. Retrieve: get top-k chunks (with metadata) from your vector store
    try:    
        chunks = vector_store().similarity_search(
            query=question,
            k=k,
        )
        
        # 2. Guard: if nothing relevant came back, return early
        #    (decide: empty list? a similarity score threshold?)
        if not chunks:
            return {"answer": "I couldn't find this in the provided documents.", "sources": []}

        # 3. Build the prompt: reuse build_user_message(chunks, question)
        llm = generator.get_llm()

        prompt = generator.build_user_message(chunks=chunks,question=question)
        # 4. Call the LLM: SystemMessage + HumanMessage via get_llm().invoke(...)
        messages = [
        SystemMessage(content=generator.system_prompt),
        HumanMessage(content=prompt)]
        
        response = llm.invoke(messages)
        # 5. Return a structured result, not just a string

        return {
            "answer": response,
            "sources": [response],   # source file, page, chunk id
        }
    except Exception as e:
        print(f"error occured at rag pipeline: {e}")

    