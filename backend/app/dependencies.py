from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    request_id = getattr(request.state, "request_id", "unknown")
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": "AUTH_REQUIRED", "message": "Bearer authentication is required", "request_id": request_id})
    try:
        payload = decode_access_token(credentials.credentials)
        user = db.scalar(select(User).where(User.id == payload["sub"]))
    except (ValueError, KeyError, TypeError):
        user = None
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": "AUTH_INVALID", "message": "Authentication credentials are invalid", "request_id": request_id})
    return user
