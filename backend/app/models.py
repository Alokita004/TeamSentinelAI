from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Table, Column, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(secondary=user_roles, back_populates="roles")


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    roles: Mapped[list[Role]] = relationship(secondary=user_roles, back_populates="users")


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    disaster_type: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    severity: Mapped[str] = mapped_column(String(30), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    signal_provider: Mapped[str] = mapped_column(String(100), nullable=False)


class AffectedZone(Base):
    __tablename__ = "affected_zones"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    incident_id: Mapped[str | None] = mapped_column(ForeignKey("incidents.id", ondelete="CASCADE"), nullable=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(30), nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)


class Shelter(Base):
    __tablename__ = "shelters"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    available: Mapped[int] = mapped_column(Integer, nullable=False)


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit: Mapped[str] = mapped_column(String(40), nullable=False)


class AgentExecution(Base):
    __tablename__ = "agent_executions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class AgentEvent(Base):
    __tablename__ = "agent_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("agent_executions.id", ondelete="CASCADE"), nullable=False, index=True)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    agent_name: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    message: Mapped[str] = mapped_column(String(240), nullable=False)
    output_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("agent_executions.id", ondelete="CASCADE"), nullable=False, index=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(nullable=False)


class EvacuationRoute(Base):
    __tablename__ = "evacuation_routes"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    source_zone_id: Mapped[str] = mapped_column(String(80), nullable=False)
    destination_shelter_id: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    score: Mapped[float] = mapped_column(nullable=False)
    distance_km: Mapped[float] = mapped_column(nullable=False)
    eta_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    blocked_reason: Mapped[str | None] = mapped_column(String(160), nullable=True)


class ResourceAllocation(Base):
    __tablename__ = "resource_allocations"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    resource_id: Mapped[str] = mapped_column(String(80), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class DecisionRecord(Base):
    __tablename__ = "decision_records"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    capacity_shortfall: Mapped[int] = mapped_column(Integer, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    actor_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    resource: Mapped[str] = mapped_column(String(160), nullable=False)
    request_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    outcome: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
