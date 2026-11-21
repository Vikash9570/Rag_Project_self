"""Turn text into vectors with the configured sentence-transformers model."""

from langchain_huggingface import HuggingFaceEmbeddings
# from backend.app.config import embedding_model
from backend.app.services.chunker import convertTochunks
from backend.app.config import settings
from backend.app.services import chunker,generator,loader
from langchain_chroma import Chroma


def get_embeddings()->HuggingFaceEmbeddings:
    try:
        return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        )
    except Exception as e:
        print(f'exception occured at getting embeddings module with error: {e}')

    





 
