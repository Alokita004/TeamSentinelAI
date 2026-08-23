from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.assistant.service import AssistantService
from app.db import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import AssistantRequest, AssistantResponse
from app.services.audit import record_audit

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/ask", response_model=AssistantResponse)
def ask(payload: AssistantRequest, request: Request, current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> AssistantResponse:
    response = AssistantResponse.model_validate(AssistantService().answer(db, payload.question))
    record_audit(db, actor_id=current_user.id, action="assistant.ask", resource="incident-flood-042", request_id=request.state.request_id, outcome="success")
    return response
