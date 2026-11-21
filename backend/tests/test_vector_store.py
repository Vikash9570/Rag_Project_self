from backend.app.services.vector_store import get_store
from langchain_core.vectorstores import VectorStore
from pathlib import Path
word='word'*50

temp_path = Path('backend/tests')

def test_store()->VectorStore:
    ...  
