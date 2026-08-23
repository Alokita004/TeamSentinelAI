from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class FloodSignal:
    provider: str
    river_level_m: float
    threshold_m: float
    observed_at: str
    severity: str


class WeatherProvider(Protocol):
    def get_flood_signal(self) -> FloodSignal: ...


class DemoWeatherProvider:
    def get_flood_signal(self) -> FloodSignal:
        return FloodSignal(provider="demo-river-gauges", river_level_m=4.8, threshold_m=4.0, observed_at="2026-08-20T14:30:00Z", severity="high")
