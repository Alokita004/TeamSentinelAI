from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AffectedZone, Incident, Resource, Shelter
from app.services.evacuation import EvacuationService


class AssistantService:
    def answer(self, db: Session, question: str) -> dict:
        normalized = question.lower().strip()
        incident = db.scalar(select(Incident).where(Incident.status == "active").order_by(Incident.started_at.desc()))
        if incident is None:
            return {"intent": "incident_status", "answer": "There is no active incident in the current workspace.", "tool_calls": [], "sources": [], "emergency": False}

        tools: list[dict] = []
        sources: list[str] = []
        parts: list[str] = []
        if any(word in normalized for word in ("risk", "danger", "people", "affected", "how many")):
            zones = list(db.scalars(select(AffectedZone).where(AffectedZone.incident_id == incident.id)))
            population = sum(zone.population for zone in zones)
            high_risk = sum(zone.population for zone in zones if zone.risk_level == "high")
            tools.append({"name": "risk_lookup", "status": "completed", "result": {"total_population": population, "high_risk_population": high_risk}})
            sources.append("risk_assessment:demo")
            parts.append(f"{population:,} people are in the affected zones, including {high_risk:,} in the high-risk zone.")
        if any(word in normalized for word in ("shelter", "capacity", "space", "places")):
            shelters = list(db.scalars(select(Shelter)))
            available = sum(shelter.available for shelter in shelters)
            tools.append({"name": "shelter_lookup", "status": "completed", "result": {"available": available, "shelter_count": len(shelters)}})
            sources.append("shelter_capacity:postgresql")
            parts.append(f"There are {available:,} shelter spaces available across {len(shelters)} shelters.")
        if any(word in normalized for word in ("route", "evacuate", "evacuation", "where should")):
            routes = EvacuationService().calculate(db, incident.id)
            safe_route = next((route for route in routes if route.status == "safe"), None)
            if safe_route:
                tools.append({"name": "route_lookup", "status": "completed", "result": {"route_id": safe_route.id, "eta_minutes": safe_route.eta_minutes, "destination": safe_route.destination_shelter_id}})
                sources.append("evacuation_routes:demo")
                parts.append(f"The highest-ranked safe route is {safe_route.id}, reaching {safe_route.destination_shelter_id} in {safe_route.eta_minutes} minutes.")
        if any(word in normalized for word in ("resource", "ambulance", "rescue", "water", "team")):
            resources = list(db.scalars(select(Resource).order_by(Resource.name)))
            tools.append({"name": "resource_lookup", "status": "completed", "result": {"resources": [{"name": item.name, "quantity": item.quantity, "unit": item.unit} for item in resources]}})
            sources.append("resource_inventory:postgresql")
            parts.append("Available response resources: " + ", ".join(f"{item.quantity} {item.unit} {item.name.lower()}" for item in resources) + ".")
        if not parts:
            parts.append("Urban Flood 042 is active with high severity. Ask about risk, shelters, evacuation routes, or resources.")
        emergency = any(word in normalized for word in ("emergency", "urgent", "immediately", "evacuate now"))
        return {"intent": "emergency_response" if emergency else "operational_lookup", "answer": " ".join(parts), "tool_calls": tools, "sources": sources, "emergency": emergency}
