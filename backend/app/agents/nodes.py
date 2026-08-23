from collections.abc import Callable

from app.agents.state import DisasterState

AGENT_ORDER = ("AlertAgent", "RiskAgent", "ImpactAgent", "GraphAgent", "RouteAgent", "ResourceAgent", "DecisionAgent", "NotificationAgent")


def _event(agent_name: str, message: str, output: dict, sequence: int) -> dict:
    return {"sequence": sequence, "agent_name": agent_name, "status": "completed", "message": message, "output": output}


def alert_agent(state: DisasterState) -> dict:
    return {"agent_events": [_event("AlertAgent", "Flood signal confirmed and incident acknowledged.", {"severity": state["incident"]["severity"]}, 1)]}


def risk_agent(state: DisasterState) -> dict:
    high_risk_population = sum(zone["population"] for zone in state["affected_zones"] if zone["risk_level"] == "high")
    return {"risk_assessment": {"level": "severe", "score": 0.92, "rationale": f"River signal exceeds threshold; {high_risk_population} people are in high-risk zones."}, "agent_events": [_event("RiskAgent", "Risk assessment completed.", {"score": 0.92, "level": "severe"}, 2)]}


def impact_agent(state: DisasterState) -> dict:
    total_population = sum(zone["population"] for zone in state["affected_zones"])
    return {"agent_events": [_event("ImpactAgent", "Affected population and zones estimated.", {"affected_population": total_population, "zone_count": len(state["affected_zones"])}, 3)]}


def graph_agent(state: DisasterState) -> dict:
    context = state.get("graph_context") or {"status": "unavailable", "zones": [], "shelters": []}
    related_entities = len(context.get("zones", [])) + len(context.get("shelters", []))
    status = context.get("status", "unavailable")
    return {"graph_context": context, "agent_events": [_event("GraphAgent", f"Graph context status: {status}.", {"related_entities": related_entities, "graph_status": status}, 4)]}


def route_agent(state: DisasterState) -> dict:
    return {"routes": [{"id": "route-northbank-shelter-02", "status": "candidate", "destination": "shelter-02"}], "agent_events": [_event("RouteAgent", "Candidate evacuation route prepared.", {"route_count": 1}, 5)]}


def resource_agent(state: DisasterState) -> dict:
    return {"resources": [{"id": "resource-rescue-01", "status": "available", "quantity": 4}], "agent_events": [_event("ResourceAgent", "Response resources matched to incident.", {"allocation_count": 1}, 6)]}


def decision_agent(state: DisasterState) -> dict:
    return {"recommendations": [{"priority": 1, "title": "Initiate Northbank evacuation", "rationale": "Move high-risk residents toward Shelter S-02 before water levels peak.", "confidence": 0.964}], "agent_events": [_event("DecisionAgent", "Priority recommendation issued.", {"recommendation_count": 1}, 7)]}


def notification_agent(state: DisasterState) -> dict:
    return {"notifications": [{"channel": "demo", "status": "prepared", "audience": "emergency_director"}], "agent_events": [_event("NotificationAgent", "Demo notification prepared for review.", {"notification_count": 1}, 8)]}


AGENT_NODES: dict[str, Callable[[DisasterState], dict]] = {
    "AlertAgent": alert_agent,
    "RiskAgent": risk_agent,
    "ImpactAgent": impact_agent,
    "GraphAgent": graph_agent,
    "RouteAgent": route_agent,
    "ResourceAgent": resource_agent,
    "DecisionAgent": decision_agent,
    "NotificationAgent": notification_agent,
}
