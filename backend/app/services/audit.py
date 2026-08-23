from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import AuditLog


def record_audit(db: Session, *, actor_id: str | None, action: str, resource: str, request_id: str, outcome: str) -> None:
    db.add(AuditLog(id=str(uuid4()), actor_id=actor_id, action=action, resource=resource, request_id=request_id, outcome=outcome))
    db.commit()
