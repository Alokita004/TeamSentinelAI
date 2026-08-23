from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import AffectedZone, EvacuationRoute, Shelter


@dataclass(frozen=True)
class RouteCandidate:
    id: str
    source_zone_id: str
    destination_shelter_id: str
    distance_km: float
    eta_minutes: int
    safety_score: float


class EvacuationService:
    candidates = (
        RouteCandidate("route-northbank-shelter-02", "zone-northbank-04", "shelter-02", 1.8, 12, 0.94),
        RouteCandidate("route-northbank-shelter-03", "zone-northbank-04", "shelter-03", 3.4, 21, 0.78),
        RouteCandidate("route-eastquay-shelter-03", "zone-northbank-05", "shelter-03", 1.2, 9, 0.91),
        RouteCandidate("route-south-shelter-03", "zone-south-02", "shelter-03", 2.6, 16, 0.86),
    )

    def calculate(self, db: Session, incident_id: str, blocked_route_ids: set[str] | None = None) -> list[EvacuationRoute]:
        blocked_route_ids = blocked_route_ids or set()
        zones = {zone.id: zone for zone in db.scalars(select(AffectedZone).where(AffectedZone.incident_id == incident_id))}
        shelters = {shelter.id: shelter for shelter in db.scalars(select(Shelter))}
        db.execute(delete(EvacuationRoute).where(EvacuationRoute.incident_id == incident_id))
        routes: list[EvacuationRoute] = []
        for candidate in self.candidates:
            if candidate.source_zone_id not in zones or candidate.destination_shelter_id not in shelters:
                continue
            is_blocked = candidate.id in blocked_route_ids
            route = EvacuationRoute(id=candidate.id, incident_id=incident_id, source_zone_id=candidate.source_zone_id, destination_shelter_id=candidate.destination_shelter_id, status="blocked" if is_blocked else "safe", score=candidate.safety_score, distance_km=candidate.distance_km, eta_minutes=candidate.eta_minutes, blocked_reason="Demo hazard closure" if is_blocked else None)
            db.add(route)
            routes.append(route)
        db.commit()
        return sorted(routes, key=lambda route: (route.status != "safe", -route.score, route.eta_minutes))
