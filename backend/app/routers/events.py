import asyncio
import json
from collections.abc import AsyncIterator
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select

from app.db import SessionLocal
from app.dependencies import get_current_user
from app.models import AgentEvent, AgentExecution, User
from app.services.orchestration import OrchestrationService

router = APIRouter(prefix="/events", tags=["real-time"])


def _run_execution(execution_id: str) -> None:
    with SessionLocal() as db:
        try:
            OrchestrationService().execute(db, "incident-flood-042", execution_id=execution_id)
        except Exception:
            db.rollback()


@router.get("/flood")
async def flood_events(request: Request, _: User = Depends(get_current_user)) -> StreamingResponse:
    execution_id = str(uuid4())
    task = asyncio.create_task(asyncio.to_thread(_run_execution, execution_id))

    async def stream() -> AsyncIterator[str]:
        last_sequence = 0
        try:
            while True:
                if await request.is_disconnected():
                    task.cancel()
                    return
                with SessionLocal() as db:
                    events = list(db.scalars(select(AgentEvent).where(AgentEvent.execution_id == execution_id, AgentEvent.sequence > last_sequence).order_by(AgentEvent.sequence)))
                    execution = db.get(AgentExecution, execution_id)
                for event in events:
                    last_sequence = event.sequence
                    payload = {"execution_id": execution_id, "sequence": event.sequence, "agent_name": event.agent_name, "status": event.status, "message": event.message, "output": json.loads(event.output_json)}
                    yield f"id: {event.sequence}\nevent: agent_event\ndata: {json.dumps(payload)}\n\n"
                if execution is not None and execution.status in {"completed", "failed"} and (not events or last_sequence == max((item.sequence for item in events), default=last_sequence)):
                    payload = {"execution_id": execution_id, "status": execution.status}
                    yield f"event: execution_complete\ndata: {json.dumps(payload)}\n\n"
                    return
                yield ": heartbeat\n\n"
                await asyncio.sleep(0.2)
        finally:
            if not task.done():
                task.cancel()

    return StreamingResponse(stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"})
