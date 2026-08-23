from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import Base, engine, init_db
from app.models import Role, User
from app.routers import assistant, auth, demo, events, graph, health, operations, orchestration
from app.schemas import ErrorResponse
from app.security import hash_password
from app.services.demo import DemoService
from app.middleware import security_middleware


def seed_demo_identity() -> None:
    settings = get_settings()
    with Session(engine) as db:
        role = db.scalar(select(Role).where(Role.name == "emergency_director"))
        if role is None:
            role = Role(name="emergency_director")
            db.add(role)
            db.flush()
        user = db.scalar(select(User).where(User.email == settings.demo_admin_email.lower()))
        if user is None:
            user = User(email=settings.demo_admin_email.lower(), password_hash=hash_password(settings.demo_admin_password), roles=[role])
            db.add(user)
        elif role not in user.roles:
            user.roles.append(role)
        db.commit()
        DemoService().reset(db)


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    seed_demo_identity()
    yield


settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.middleware("http")(security_middleware)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, _: RequestValidationError):
    payload = ErrorResponse(code="VALIDATION_ERROR", message="Request validation failed", request_id=request.state.request_id)
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, _: Exception):
    payload = ErrorResponse(code="INTERNAL_ERROR", message="An unexpected error occurred", request_id=request.state.request_id)
    return JSONResponse(status_code=500, content=payload.model_dump())


app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(demo.router, prefix="/api/v1")
app.include_router(orchestration.router, prefix="/api/v1")
app.include_router(graph.router, prefix="/api/v1")
app.include_router(operations.router, prefix="/api/v1")
app.include_router(events.router, prefix="/api/v1")
app.include_router(assistant.router, prefix="/api/v1")
