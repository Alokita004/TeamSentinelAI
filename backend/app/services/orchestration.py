import json
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents.graph import DISASTER_GRAPH
from app.agents.state import DisasterState
from app.models import AffectedZone, AgentEvent, AgentExecution, Incident, Recommendation
from app.services.graph import GraphService


class OrchestrationService:
    def execute(self, db: Session, incident_id: str, execution_id: str | None = None) -> AgentExecution:
        incident = db.get(Incident, incident_id)
        if incident is None or incident.status != "active":
            raise ValueError("An active incident is required before orchestration")
        zones = list(db.scalars(select(AffectedZone).where(AffectedZone.incident_id == incident_id).order_by(AffectedZone.id)))
        graph_service = GraphService()
        graph_service.project_flood(db, incident_id)
        graph_context = graph_service.incident_context(incident_id)
        execution = AgentExecution(id=execution_id or str(uuid4()), incident_id=incident_id, status="running", started_at=datetime.now(timezone.utc), error_count=0)
        db.add(execution)
        db.commit()
        state: DisasterState = {
            "incident": {"id": incident.id, "name": incident.name, "disaster_type": incident.disaster_type, "severity": incident.severity},
            "risk_assessment": None,
            "affected_zones": [{"id": zone.id, "name": zone.name, "risk_level": zone.risk_level, "population": zone.population} for zone in zones],
            "graph_context": graph_context,
            "routes": [],
            "resources": [],
            "recommendations": [],
            "notifications": [],
            "agent_events": [],
            "errors": [],
        }
        try:
            result = dict(state)
            for update in DISASTER_GRAPH.stream(state, stream_mode="updates"):
                node_output = next(iter(update.values()))
                for key, value in node_output.items():
                    if key == "agent_events":
                        result[key] = result.get(key, []) + value
                        for event in value:
                            db.add(AgentEvent(id=str(uuid4()), execution_id=execution.id, sequence=event["sequence"], agent_name=event["agent_name"], status=event["status"], message=event["message"], output_json=json.dumps(event["output"], sort_keys=True)))
                        db.commit()
                    else:
                        result[key] = value
            for recommendation in result["recommendations"]:
                db.add(Recommendation(id=str(uuid4()), execution_id=execution.id, priority=recommendation["priority"], title=recommendation["title"], rationale=recommendation["rationale"], confidence=recommendation["confidence"]))
            execution.status = "completed"
            execution.completed_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(execution)
            return execution
        except Exception:
            execution.status = "failed"
            execution.error_count = 1
            execution.completed_at = datetime.now(timezone.utc)
            db.commit()
            raise

    def details(self, db: Session, execution_id: str) -> dict:
        execution = db.get(AgentExecution, execution_id)
        if execution is None:
            raise ValueError("Execution not found")
        events = list(db.scalars(select(AgentEvent).where(AgentEvent.execution_id == execution_id).order_by(AgentEvent.sequence)))
        recommendations = list(db.scalars(select(Recommendation).where(Recommendation.execution_id == execution_id).order_by(Recommendation.priority)))
        return {"execution": execution, "events": events, "recommendations": recommendations}
