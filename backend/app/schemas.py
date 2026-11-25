from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    message: str
    chunks: int


class AskRequest(BaseModel):
    question: str = Field(min_length=1)


class Source(BaseModel):
    text: str
    source: str
    page: int | None = None


class AskResponse(BaseModel):
    answer: str
    cited_ids: list[str]
