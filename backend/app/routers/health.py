from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.schemas import HealthResponse, ReadinessResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service=settings.app_name, environment=settings.environment)


@router.get("/readiness", response_model=ReadinessResponse)
def readiness(db: Session = Depends(get_db)) -> ReadinessResponse:
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return ReadinessResponse(status="not_ready", database="error")
    return ReadinessResponse(status="ready", database="ok")
