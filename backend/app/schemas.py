from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: str


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    environment: str


class ReadinessResponse(BaseModel):
    status: Literal["ready", "not_ready"]
    database: Literal["ok", "error"]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=256)


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    is_active: bool
    roles: list[str]
    created_at: datetime


class FloodZoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    risk_level: str
    population: int


class ShelterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    capacity: int
    available: int


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    quantity: int
    unit: str


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    disaster_type: str
    name: str
    status: str
    severity: str
    started_at: datetime | None
    signal_provider: str


class DemoSnapshotResponse(BaseModel):
    mode: Literal["demo"]
    incident: IncidentResponse | None
    zones: list[FloodZoneResponse]
    shelters: list[ShelterResponse]
    resources: list[ResourceResponse]


class DemoActionResponse(BaseModel):
    action: Literal["simulated", "reset"]
    snapshot: DemoSnapshotResponse


class AgentEventResponse(BaseModel):
    sequence: int
    agent_name: str
    status: str
    message: str
    output: dict


class RecommendationResponse(BaseModel):
    priority: int
    title: str
    rationale: str
    confidence: float


class ExecutionResponse(BaseModel):
    id: str
    incident_id: str
    status: str
    started_at: datetime
    completed_at: datetime | None
    error_count: int
    events: list[AgentEventResponse]
    recommendations: list[RecommendationResponse]


class RouteRequest(BaseModel):
    blocked_route_ids: list[str] = Field(default_factory=list)


class RouteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source_zone_id: str
    destination_shelter_id: str
    status: str
    score: float
    distance_km: float
    eta_minutes: int
    blocked_reason: str | None


class AllocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    resource_id: str
    quantity: int
    status: str


class DecisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    summary: str
    status: str
    capacity_shortfall: int


class OperationsResponse(BaseModel):
    incident_id: str
    routes: list[RouteResponse]
    allocations: list[AllocationResponse]
    decision: DecisionResponse


class AssistantRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


class AssistantToolCall(BaseModel):
    name: str
    status: str
    result: dict


class AssistantResponse(BaseModel):
    intent: str
    answer: str
    tool_calls: list[AssistantToolCall]
    sources: list[str]
    emergency: bool
