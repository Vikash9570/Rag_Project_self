"""Read PDF / TXT / MD / DOCX files into raw text plus page metadata."""
import hashlib

import os
import tempfile
import shutil
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.exception import *
# import vector_store

# importing file from local dir

def load_document(local_path:str,source:str)->dict:
    # give proper path
    try:
        pages = PyPDFLoader(local_path).load()
        # print(f"from root function pages {pages[0]}")

    except Exception as e:
        raise IngestionError(f'error occured at loader.py while loading the pdf: {e}')

    # adding metadata
    for page in pages:
        page.metadata['source'] = source

        # adding index
    for page in pages:
        page_num=page.metadata["page"]
        page.metadata["page"]=page_num+1

    # returning pages
    return pages
   


if __name__ == "__main__":
    pdf_path = Path(__file__).resolve().parents[3] / "backend" / "data" / "uploads" / "Abstract.pdf"
    print(load_document(str(pdf_path)))





