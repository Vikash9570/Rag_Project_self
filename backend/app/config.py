from pathlib import Path
import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


BACKEND_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    """All tunable values live here. Override any of them via .env."""

    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")

    # LLM
    OPENROUTER_API_KEY: str = os.environ["OPENROUTER_API_KEY"]
    llm_model: str = "baidu/ernie-5.5-flash-preview:free"

    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"

    # Chunking (measured in characters) and retrieval
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 4

    # Storage
    upload_dir: Path = BACKEND_DIR / "data" / "uploads"
    vector_db_dir: Path = BACKEND_DIR / "data" / "vector_db"

    # The frontend is opened straight from disk (origin "null"), so allow all
    # origins during development. Restrict this before deploying.
    cors_origins: list[str] = ["*"]

    # db collection name
    collection_name :str = 'Sample'

settings = Settings()
