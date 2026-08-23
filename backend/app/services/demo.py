from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import AffectedZone, Incident, Resource, Shelter
from app.schemas import DemoSnapshotResponse, IncidentResponse, ResourceResponse, ShelterResponse, FloodZoneResponse
from app.strategies.flood import FloodStrategy


class DemoService:
    def __init__(self, strategy: FloodStrategy | None = None) -> None:
        self.strategy = strategy or FloodStrategy()

    def reset(self, db: Session) -> DemoSnapshotResponse:
        db.execute(delete(AffectedZone))
        db.execute(delete(Incident))
        db.execute(delete(Shelter))
        db.execute(delete(Resource))
        for fixture in self.strategy.zones():
            db.add(AffectedZone(id=fixture.id, name=fixture.name, risk_level=fixture.risk_level, population=fixture.population))
        for fixture in self.strategy.shelters():
            db.add(Shelter(id=fixture.id, name=fixture.name, capacity=fixture.capacity, available=fixture.available))
        for fixture in self.strategy.resources():
            db.add(Resource(id=fixture.id, name=fixture.name, quantity=fixture.quantity, unit=fixture.unit))
        db.commit()
        return self.snapshot(db)

    def simulate(self, db: Session) -> DemoSnapshotResponse:
        snapshot = self.snapshot(db)
        if snapshot.incident is not None and snapshot.incident.status == "active":
            return snapshot
        if not snapshot.zones or not snapshot.shelters or not snapshot.resources:
            self.reset(db)
        signal = self.strategy.signal()
        incident = Incident(id=self.strategy.incident_id, disaster_type="flood", name="Urban Flood 042", status="active", severity=signal.severity, started_at=datetime.fromisoformat(signal.observed_at.replace("Z", "+00:00")), signal_provider=signal.provider)
        db.add(incident)
        for zone in self.strategy.zones():
            existing = db.get(AffectedZone, zone.id)
            existing.incident_id = incident.id
        db.commit()
        return self.snapshot(db)

    def snapshot(self, db: Session) -> DemoSnapshotResponse:
        incident = db.scalar(select(Incident).where(Incident.id == self.strategy.incident_id))
        zones = list(db.scalars(select(AffectedZone).order_by(AffectedZone.id)))
        shelters = list(db.scalars(select(Shelter).order_by(Shelter.id)))
        resources = list(db.scalars(select(Resource).order_by(Resource.id)))
        incident_response = None
        if incident:
            started_at = incident.started_at
            if started_at is not None and started_at.tzinfo is None:
                started_at = started_at.replace(tzinfo=timezone.utc)
            incident_response = IncidentResponse(
                id=incident.id,
                disaster_type=incident.disaster_type,
                name=incident.name,
                status=incident.status,
                severity=incident.severity,
                started_at=started_at,
                signal_provider=incident.signal_provider,
            )
        return DemoSnapshotResponse(
            mode="demo",
            incident=incident_response,
            zones=[FloodZoneResponse.model_validate(zone) for zone in zones],
            shelters=[ShelterResponse.model_validate(shelter) for shelter in shelters],
            resources=[ResourceResponse.model_validate(resource) for resource in resources],
        )
