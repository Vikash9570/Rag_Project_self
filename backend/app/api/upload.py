from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas import UploadResponse

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)) -> UploadResponse:
    # TODO: save file -> loader -> chunker -> embedder -> vector_store.add
    raise HTTPException(status_code=501, detail="Upload pipeline not implemented yet")
