from fastapi import APIRouter, HTTPException

from app.schemas import AskRequest, AskResponse

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    # TODO: embedder(question) -> vector_store.search -> generator -> answer + sources
    raise HTTPException(status_code=501, detail="Ask pipeline not implemented yet")
