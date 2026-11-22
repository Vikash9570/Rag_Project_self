from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.schemas import UploadResponse
from backend.app.services import ingestion,vector_store
from backend.app import config
from pathlib import Path
import shutil

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
def upload_endpoint(file: UploadFile = File(...)) -> UploadResponse:
    # validating if not pdf file
    if file.filename.suffix.lower() not in ('.pdf') or not file.filename:
        raise HTTPException(status_code=400, detail="Upload file is not .pdf")

    # saving to upload_dir
    upload_dir = config.settings.upload_dir
    
    safe_name = Path(file.filename).name
    upload_dir.mkdir(parents=True,exist_ok=True)
    destination = upload_dir/safe_name

    try:
       with destination.open("wb") as buffer:
           shutil.copyfileobj(file.file,buffer)
    finally:
        file.file.close()

    summary = ingestion.ingest(config.settings.upload_dir, vector_store.get_store())

    if not summary:
        raise HTTPException(status_code=501, detail="Upload pipeline not implemented yet")
    
    return UploadResponse(message="file has been added successfully", chunks= summary['chunks_added'])


    

    
