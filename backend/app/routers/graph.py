from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import User
from app.services.graph import GraphService

router = APIRouter(prefix="/graph", tags=["knowledge graph"])


@router.get("/status")
def status(_: Annotated[User, Depends(get_current_user)]) -> dict[str, str]:
    return GraphService().status()


@router.post("/incidents/{incident_id}/project")
def project(incident_id: str, _: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> dict:
    return GraphService().project_flood(db, incident_id)


@router.get("/incidents/{incident_id}/context")
def context(incident_id: str, _: Annotated[User, Depends(get_current_user)]) -> dict:
    return GraphService().incident_context(incident_id)
