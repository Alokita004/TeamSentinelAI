from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import DemoActionResponse, DemoSnapshotResponse
from app.services.demo import DemoService

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/snapshot", response_model=DemoSnapshotResponse)
def snapshot(_: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> DemoSnapshotResponse:
    return DemoService().snapshot(db)


@router.post("/flood/simulate", response_model=DemoActionResponse)
def simulate(_: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> DemoActionResponse:
    return DemoActionResponse(action="simulated", snapshot=DemoService().simulate(db))


@router.post("/reset", response_model=DemoActionResponse)
def reset(_: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> DemoActionResponse:
    return DemoActionResponse(action="reset", snapshot=DemoService().reset(db))
