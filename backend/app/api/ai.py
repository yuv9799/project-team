from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.schemas.schemas import AIProjectInput
from app.services.ai import extract_project

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/extract-project-requirements")
def extract(data: AIProjectInput, _=Depends(get_current_user)):
    return extract_project(data.text)
