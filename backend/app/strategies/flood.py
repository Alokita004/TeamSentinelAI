from dataclasses import dataclass

from app.providers.ports import DemoWeatherProvider, FloodSignal


@dataclass(frozen=True)
class FloodZoneFixture:
    id: str
    name: str
    risk_level: str
    population: int


@dataclass(frozen=True)
class ShelterFixture:
    id: str
    name: str
    capacity: int
    available: int


@dataclass(frozen=True)
class ResourceFixture:
    id: str
    name: str
    quantity: int
    unit: str


class FloodStrategy:
    name = "urban_flood"
    incident_id = "incident-flood-042"

    def __init__(self) -> None:
        self.weather = DemoWeatherProvider()

    def signal(self) -> FloodSignal:
        return self.weather.get_flood_signal()

    def zones(self) -> tuple[FloodZoneFixture, ...]:
        return (
            FloodZoneFixture("zone-northbank-04", "Northbank", "high", 4200),
            FloodZoneFixture("zone-northbank-05", "East Quay", "moderate", 3180),
            FloodZoneFixture("zone-south-02", "South District", "moderate", 5100),
        )

    def shelters(self) -> tuple[ShelterFixture, ...]:
        return (
            ShelterFixture("shelter-02", "Northbank Civic Shelter", 2800, 2140),
            ShelterFixture("shelter-03", "East Quay School", 1700, 1210),
        )

    def resources(self) -> tuple[ResourceFixture, ...]:
        return (
            ResourceFixture("resource-ambulance-01", "Ambulances", 12, "vehicles"),
            ResourceFixture("resource-rescue-01", "Rescue teams", 4, "teams"),
            ResourceFixture("resource-water-01", "Drinking water", 8400, "litres"),
        )
