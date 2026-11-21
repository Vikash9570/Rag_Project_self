"""Split loaded text into overlapping chunks (size and overlap come from config)."""

from backend.app.config import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# defining text splitter



def convertTochunks(documents:list[Document])->list[Document]:
    """Split the documents into chunks"""
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = settings.chunk_size,
            chunk_overlap = settings.chunk_overlap
        )
        return splitter.split_documents(documents)
    except Exception as e:
        print (f'error occured at convert to chunk: {e}')

