"""Turn text into vectors with the configured sentence-transformers model."""

from langchain_huggingface import HuggingFaceEmbeddings
from backend.app.config import settings
from functools import lru_cache


@lru_cache(max=1)
def get_embeddings()->HuggingFaceEmbeddings:
    try:
        return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        )
    except Exception as e:
        print(f'exception occured at getting embeddings module with error: {e}')

    





 
