from fastapi import APIRouter, HTTPException

from backend.app.schemas import AskRequest, AskResponse
from backend.app.services import rag_pipeline
#  for evaluation purpose response
from eval import run_eval

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_endpoint(req: AskRequest) -> AskResponse:
    try:
        result = rag_pipeline.ask(req.question)
        return AskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Ask pipeline not implemented yet{e}")


# for evaluation purpose
@router.post("/ask_eval", response_model=AskResponse)
def ask_eval(req: AskRequest) -> AskResponse:
    try:
        result = run_eval.ask(req.question)
        return AskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Ask pipeline not implemented yet{e}")

