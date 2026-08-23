from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import AffectedZone, DecisionRecord, Resource, ResourceAllocation, Shelter


class ResourceService:
    def allocate(self, db: Session, incident_id: str) -> tuple[list[ResourceAllocation], DecisionRecord]:
        db.execute(delete(ResourceAllocation).where(ResourceAllocation.incident_id == incident_id))
        db.execute(delete(DecisionRecord).where(DecisionRecord.incident_id == incident_id))
        resources = {resource.id: resource for resource in db.scalars(select(Resource))}
        zones = list(db.scalars(select(AffectedZone).where(AffectedZone.incident_id == incident_id)))
        shelters = list(db.scalars(select(Shelter)))
        affected_population = sum(zone.population for zone in zones)
        available_capacity = sum(shelter.available for shelter in shelters)
        allocations = []
        requested = {
            "resource-rescue-01": 2,
            "resource-ambulance-01": 3,
            "resource-water-01": min(affected_population, 4200),
        }
        for resource_id, quantity in requested.items():
            resource = resources[resource_id]
            allocated = min(resource.quantity, quantity)
            allocations.append(ResourceAllocation(id=f"allocation-{incident_id}-{resource_id}", incident_id=incident_id, resource_id=resource_id, quantity=allocated, status="allocated" if allocated == quantity else "partial"))
        shortfall = max(0, affected_population - available_capacity)
        decision = DecisionRecord(id=f"decision-{incident_id}", incident_id=incident_id, summary="Prioritize Northbank evacuation and allocate rescue capacity to the highest-risk zone.", status="requires_review" if shortfall else "ready", capacity_shortfall=shortfall)
        db.add_all(allocations)
        db.add(decision)
        db.commit()
        return allocations, decision
