from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ask, upload
from app.config import settings

settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.vector_db_dir.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="RAG End to End")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(upload.router)
app.include_router(ask.router)
