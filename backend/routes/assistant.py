from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

from backend.services.rag_service import answer_question

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)

    @field_validator("question", mode="before")
    @classmethod
    def trim_question(cls, value):
        return value.strip() if isinstance(value, str) else value


@router.post("/ask")
def ask_research_assistant(request: QuestionRequest):
    return answer_question(request.question)
