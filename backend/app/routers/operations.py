from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import AllocationResponse, DecisionResponse, OperationsResponse, RouteRequest, RouteResponse
from app.services.evacuation import EvacuationService
from app.services.resources import ResourceService

router = APIRouter(prefix="/operations", tags=["evacuation and resources"])


@router.post("/{incident_id}/plan", response_model=OperationsResponse)
def plan(incident_id: str, payload: RouteRequest, _: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> OperationsResponse:
    try:
        routes = EvacuationService().calculate(db, incident_id, set(payload.blocked_route_ids))
        allocations, decision = ResourceService().allocate(db, incident_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"code": "DEMO_DATA_REQUIRED", "message": f"Missing resource fixture: {error.args[0]}", "request_id": "operations"}) from error
    return OperationsResponse(
        incident_id=incident_id,
        routes=[RouteResponse.model_validate(route) for route in routes],
        allocations=[AllocationResponse.model_validate(item) for item in allocations],
        decision=DecisionResponse.model_validate(decision),
    )


@router.get("/{incident_id}/routes", response_model=list[RouteResponse])
def routes(incident_id: str, _: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> list[RouteResponse]:
    return [RouteResponse.model_validate(route) for route in EvacuationService().calculate(db, incident_id)]
