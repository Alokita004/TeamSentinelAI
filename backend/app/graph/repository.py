from collections.abc import Iterable
from contextlib import contextmanager
from typing import Any

from app.config import get_settings
from app.graph.queries import CONSTRAINTS, INCIDENT_CONTEXT, PROJECT_FLOOD


class GraphUnavailableError(RuntimeError):
    pass


class Neo4jRepository:
    def __init__(self) -> None:
        self._driver = None
        self._import_error: str | None = None
        try:
            from neo4j import GraphDatabase

            settings = get_settings()
            if not settings.neo4j_uri:
                self._import_error = "Neo4j URI is not configured"
            else:
                self._driver = GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))
        except ImportError:
            self._import_error = "Neo4j driver is not installed"

    @property
    def available(self) -> bool:
        return self._driver is not None

    @property
    def unavailable_reason(self) -> str | None:
        return self._import_error

    @contextmanager
    def session(self):
        if self._driver is None:
            raise GraphUnavailableError(self._import_error or "Neo4j is unavailable")
        with self._driver.session() as session:
            yield session

    def close(self) -> None:
        if self._driver is not None:
            self._driver.close()

    def ensure_schema(self) -> None:
        with self.session() as session:
            for statement in CONSTRAINTS:
                session.run(statement).consume()

    def project_flood(self, incident_id: str, zones: Iterable[dict[str, Any]], shelters: Iterable[dict[str, Any]]) -> dict[str, Any]:
        with self.session() as session:
            result = session.run(PROJECT_FLOOD, incident_id=incident_id, zones=list(zones), shelters=list(shelters)).single()
            return dict(result) if result else {"incident_id": incident_id, "shelter_count": 0}

    def incident_context(self, incident_id: str) -> dict[str, Any]:
        with self.session() as session:
            result = session.run(INCIDENT_CONTEXT, incident_id=incident_id).single()
            if result is None:
                return {"incident_id": incident_id, "zones": [], "shelters": []}
            return dict(result)
