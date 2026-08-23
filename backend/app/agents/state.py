import operator
from typing import Annotated, TypedDict
from typing_extensions import NotRequired


class IncidentData(TypedDict):
    id: str
    name: str
    disaster_type: str
    severity: str


class RiskAssessment(TypedDict):
    level: str
    score: float
    rationale: str


class AffectedZoneData(TypedDict):
    id: str
    name: str
    risk_level: str
    population: int


class RecommendationData(TypedDict):
    priority: int
    title: str
    rationale: str
    confidence: float


class AgentEventData(TypedDict):
    sequence: int
    agent_name: str
    status: str
    message: str
    output: dict


class DisasterState(TypedDict):
    incident: IncidentData
    risk_assessment: NotRequired[RiskAssessment | None]
    affected_zones: list[AffectedZoneData]
    graph_context: NotRequired[dict | None]
    routes: list[dict]
    resources: list[dict]
    recommendations: list[RecommendationData]
    notifications: list[dict]
    agent_events: Annotated[list[AgentEventData], operator.add]
    errors: list[dict]
