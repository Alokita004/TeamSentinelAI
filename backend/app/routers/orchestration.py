import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import AgentEventResponse, ExecutionResponse, RecommendationResponse
from app.services.orchestration import OrchestrationService

router = APIRouter(prefix="/executions", tags=["orchestration"])


def _response(details: dict) -> ExecutionResponse:
    execution = details["execution"]
    return ExecutionResponse(
        id=execution.id,
        incident_id=execution.incident_id,
        status=execution.status,
        started_at=execution.started_at,
        completed_at=execution.completed_at,
        error_count=execution.error_count,
        events=[AgentEventResponse(sequence=event.sequence, agent_name=event.agent_name, status=event.status, message=event.message, output=json.loads(event.output_json)) for event in details["events"]],
        recommendations=[RecommendationResponse(priority=item.priority, title=item.title, rationale=item.rationale, confidence=item.confidence) for item in details["recommendations"]],
    )


@router.post("/flood", response_model=ExecutionResponse)
def execute_flood(_: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> ExecutionResponse:
    try:
        execution = OrchestrationService().execute(db, "incident-flood-042")
        return _response(OrchestrationService().details(db, execution.id))
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"code": "INCIDENT_REQUIRED", "message": str(error), "request_id": "orchestration"}) from error


@router.get("/{execution_id}", response_model=ExecutionResponse)
def execution(execution_id: str, _: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> ExecutionResponse:
    try:
        return _response(OrchestrationService().details(db, execution_id))
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "EXECUTION_NOT_FOUND", "message": str(error), "request_id": "orchestration"}) from error
