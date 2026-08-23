from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import LoginRequest, TokenResponse, UserResponse
from app.security import create_access_token, verify_password
from app.services.audit import record_audit

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Annotated[Session, Depends(get_db)]) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if user is None or not verify_password(payload.password, user.password_hash):
        record_audit(db, actor_id=None, action="auth.login", resource=payload.email.lower(), request_id=request.state.request_id, outcome="denied")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": "AUTH_INVALID", "message": "Email or password is incorrect", "request_id": request.state.request_id})
    roles = [role.name for role in user.roles]
    token, expires_in = create_access_token(user.id, roles)
    record_audit(db, actor_id=user.id, action="auth.login", resource=user.email, request_id=request.state.request_id, outcome="success")
    return TokenResponse(access_token=token, expires_in=expires_in)


@router.get("/me", response_model=UserResponse)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
    return UserResponse(id=current_user.id, email=current_user.email, is_active=current_user.is_active, roles=[role.name for role in current_user.roles], created_at=current_user.created_at)
