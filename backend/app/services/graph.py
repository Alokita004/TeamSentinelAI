from sqlalchemy import select
from sqlalchemy.orm import Session

from app.graph.repository import GraphUnavailableError, Neo4jRepository
from app.models import AffectedZone, Shelter


class GraphService:
    def __init__(self, repository: Neo4jRepository | None = None) -> None:
        self.repository = repository or Neo4jRepository()

    def status(self) -> dict[str, str]:
        if not self.repository.available:
            return {"status": "unavailable", "reason": self.repository.unavailable_reason or "Neo4j is unavailable"}
        try:
            self.repository.ensure_schema()
        except Exception as error:
            return {"status": "unavailable", "reason": str(error)}
        return {"status": "ready", "reason": "Neo4j schema is reachable"}

    def project_flood(self, db: Session, incident_id: str) -> dict:
        zones = list(db.scalars(select(AffectedZone).where(AffectedZone.incident_id == incident_id).order_by(AffectedZone.id)))
        shelters = list(db.scalars(select(Shelter).order_by(Shelter.id)))
        payload_zones = [{"id": zone.id, "name": zone.name, "risk_level": zone.risk_level, "population": zone.population} for zone in zones]
        payload_shelters = [{"id": shelter.id, "name": shelter.name, "capacity": shelter.capacity, "available": shelter.available} for shelter in shelters]
        try:
            return {"status": "projected", "freshness": "current", **self.repository.project_flood(incident_id, payload_zones, payload_shelters)}
        except GraphUnavailableError as error:
            return {"status": "unavailable", "freshness": "not_projected", "reason": str(error), "incident_id": incident_id}

    def incident_context(self, incident_id: str) -> dict:
        try:
            return {"status": "ready", "freshness": "current", **self.repository.incident_context(incident_id)}
        except GraphUnavailableError as error:
            return {"status": "unavailable", "freshness": "not_projected", "reason": str(error), "incident_id": incident_id, "zones": [], "shelters": []}
