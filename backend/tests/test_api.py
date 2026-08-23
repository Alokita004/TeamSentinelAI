import os

os.environ["DATABASE_URL"] = "sqlite:///./test_sentinelai.db"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["DEMO_ADMIN_EMAIL"] = "admin@test.example"
os.environ["DEMO_ADMIN_PASSWORD"] = "test-password"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_and_readiness() -> None:
    with client:
        assert client.get("/api/v1/health").json()["status"] == "ok"
        assert client.get("/api/v1/readiness").json() == {"status": "ready", "database": "ok"}


def test_login_and_current_user() -> None:
    with client:
        response = client.post("/api/v1/auth/login", json={"email": "admin@test.example", "password": "test-password"})
        assert response.status_code == 200
        token = response.json()["access_token"]
        me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200
        assert me.json()["email"] == "admin@test.example"
        assert me.json()["roles"] == ["emergency_director"]


def test_invalid_login_has_structured_error() -> None:
    with client:
        response = client.post("/api/v1/auth/login", json={"email": "admin@test.example", "password": "wrong"})
        assert response.status_code == 401
        body = response.json()["detail"]
        assert body["code"] == "AUTH_INVALID"
        assert body["request_id"]


def test_request_id_is_returned() -> None:
    with client:
        response = client.get("/api/v1/health", headers={"X-Request-ID": "phase2-test"})
        assert response.headers["X-Request-ID"] == "phase2-test"


def _auth_headers() -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": "admin@test.example", "password": "test-password"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_demo_reset_restores_baseline_without_incident() -> None:
    with client:
        response = client.post("/api/v1/demo/reset", headers=_auth_headers())
        assert response.status_code == 200
        snapshot = response.json()["snapshot"]
        assert snapshot["incident"] is None
        assert len(snapshot["zones"]) == 3
        assert len(snapshot["shelters"]) == 2
        assert len(snapshot["resources"]) == 3


def test_flood_simulation_is_deterministic_and_idempotent() -> None:
    with client:
        headers = _auth_headers()
        first = client.post("/api/v1/demo/flood/simulate", headers=headers).json()["snapshot"]
        second = client.post("/api/v1/demo/flood/simulate", headers=headers).json()["snapshot"]
        assert first == second
        assert first["incident"]["id"] == "incident-flood-042"
        assert first["incident"]["severity"] == "high"


def test_demo_routes_require_authentication() -> None:
    with client:
        response = client.get("/api/v1/demo/snapshot")
        assert response.status_code == 401


def test_flood_execution_persists_ordered_agent_events() -> None:
    with client:
        headers = _auth_headers()
        client.post("/api/v1/demo/flood/simulate", headers=headers)
        response = client.post("/api/v1/executions/flood", headers=headers)
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "completed"
        assert [event["agent_name"] for event in body["events"]] == [
            "AlertAgent", "RiskAgent", "ImpactAgent", "GraphAgent",
            "RouteAgent", "ResourceAgent", "DecisionAgent", "NotificationAgent",
        ]
        assert body["recommendations"][0]["title"] == "Initiate Northbank evacuation"
        details = client.get(f"/api/v1/executions/{body['id']}", headers=headers)
        assert details.status_code == 200
        assert len(details.json()["events"]) == 8


def test_flood_execution_requires_active_incident() -> None:
    with client:
        headers = _auth_headers()
        client.post("/api/v1/demo/reset", headers=headers)
        response = client.post("/api/v1/executions/flood", headers=headers)
        assert response.status_code == 409
        assert response.json()["detail"]["code"] == "INCIDENT_REQUIRED"


def test_graph_status_is_explicit_when_neo4j_is_not_configured() -> None:
    with client:
        response = client.get("/api/v1/graph/status", headers=_auth_headers())
        assert response.status_code == 200
        assert response.json()["status"] == "unavailable"


def test_graph_context_reports_unprojected_state_without_neo4j() -> None:
    with client:
        response = client.get("/api/v1/graph/incidents/incident-flood-042/context", headers=_auth_headers())
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "unavailable"
        assert body["freshness"] == "not_projected"


def test_operations_plan_ranks_safe_routes_and_allocates_resources() -> None:
    with client:
        headers = _auth_headers()
        client.post("/api/v1/demo/reset", headers=headers)
        client.post("/api/v1/demo/flood/simulate", headers=headers)
        response = client.post("/api/v1/operations/incident-flood-042/plan", headers=headers, json={"blocked_route_ids": []})
        assert response.status_code == 200
        body = response.json()
        assert body["routes"][0]["status"] == "safe"
        assert body["routes"][0]["id"] == "route-northbank-shelter-02"
        assert body["allocations"][0]["status"] == "allocated"
        assert body["decision"]["status"] == "requires_review"
        assert body["decision"]["capacity_shortfall"] == 9130


def test_operations_plan_excludes_blocked_route_from_top_rank() -> None:
    with client:
        headers = _auth_headers()
        client.post("/api/v1/demo/flood/simulate", headers=headers)
        response = client.post("/api/v1/operations/incident-flood-042/plan", headers=headers, json={"blocked_route_ids": ["route-northbank-shelter-02"]})
        assert response.status_code == 200
        routes = response.json()["routes"]
        assert routes[0]["id"] != "route-northbank-shelter-02"
        assert any(route["status"] == "blocked" for route in routes)


def test_flood_sse_stream_emits_ordered_events() -> None:
    with client:
        headers = _auth_headers()
        client.post("/api/v1/demo/flood/simulate", headers=headers)
        with client.stream("GET", "/api/v1/events/flood", headers=headers) as response:
            assert response.status_code == 200
            body = "".join(response.iter_text())
        assert "event: agent_event" in body
        assert '"agent_name": "AlertAgent"' in body
        assert '"agent_name": "NotificationAgent"' in body
        assert "event: execution_complete" in body


def test_assistant_uses_bounded_operational_tools() -> None:
    with client:
        headers = _auth_headers()
        client.post("/api/v1/demo/flood/simulate", headers=headers)
        response = client.post("/api/v1/assistant/ask", headers=headers, json={"question": "How many people are at risk and where should we evacuate?"})
        assert response.status_code == 200
        body = response.json()
        assert body["intent"] == "operational_lookup"
        assert {tool["name"] for tool in body["tool_calls"]} == {"risk_lookup", "route_lookup"}
        assert body["sources"]
        assert "12,480" in body["answer"]


def test_assistant_returns_emergency_response_with_shelter_and_resources() -> None:
    with client:
        headers = _auth_headers()
        client.post("/api/v1/demo/flood/simulate", headers=headers)
        response = client.post("/api/v1/assistant/ask", headers=headers, json={"question": "Emergency: what shelter capacity and rescue resources are available?"})
        assert response.status_code == 200
        body = response.json()
        assert body["intent"] == "emergency_response"
        assert body["emergency"] is True
        assert {tool["name"] for tool in body["tool_calls"]} == {"shelter_lookup", "resource_lookup"}


def test_assistant_question_is_size_limited() -> None:
    with client:
        response = client.post("/api/v1/assistant/ask", headers=_auth_headers(), json={"question": "x" * 1001})
        assert response.status_code == 422


def test_security_headers_and_request_id_are_present() -> None:
    with client:
        response = client.get("/api/v1/health", headers={"X-Request-ID": "hardening-test"})
        assert response.status_code == 200
        assert response.headers["X-Request-ID"] == "hardening-test"
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"


def test_oversized_request_is_rejected() -> None:
    with client:
        response = client.post("/api/v1/auth/login", headers={"Content-Length": "1000001"}, json={"email": "admin@test.example", "password": "x"})
        assert response.status_code == 413


def test_login_creates_audit_record() -> None:
    from sqlalchemy import select

    from app.db import SessionLocal
    from app.models import AuditLog

    with client:
        _auth_headers()
    with SessionLocal() as db:
        assert db.scalar(select(AuditLog).where(AuditLog.action == "auth.login")) is not None


def test_final_demo_e2e_journey() -> None:
    with client:
        login = client.post("/api/v1/auth/login", json={"email": "admin@test.example", "password": "test-password"})
        assert login.status_code == 200
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        reset = client.post("/api/v1/demo/reset", headers=headers)
        assert reset.status_code == 200 and reset.json()["snapshot"]["incident"] is None
        simulated = client.post("/api/v1/demo/flood/simulate", headers=headers)
        assert simulated.status_code == 200 and simulated.json()["snapshot"]["incident"]["id"] == "incident-flood-042"
        graph = client.get("/api/v1/graph/status", headers=headers)
        assert graph.status_code == 200
        with client.stream("GET", "/api/v1/events/flood", headers=headers) as stream:
            assert stream.status_code == 200
            event_stream = "".join(stream.iter_text())
        assert "event: execution_complete" in event_stream
        operations = client.post("/api/v1/operations/incident-flood-042/plan", headers=headers, json={"blocked_route_ids": []})
        assert operations.status_code == 200 and operations.json()["routes"]
        assistant = client.post("/api/v1/assistant/ask", headers=headers, json={"question": "What is the safest evacuation route and shelter capacity?"})
        assert assistant.status_code == 200 and assistant.json()["tool_calls"]
        final_reset = client.post("/api/v1/demo/reset", headers=headers)
        assert final_reset.status_code == 200 and final_reset.json()["snapshot"]["incident"] is None
