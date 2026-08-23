# SentinelAI API

Phase 2 provides the FastAPI backend foundation only.

## Local Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The local default database is SQLite. The Compose profile uses PostgreSQL.

## Endpoints

- `GET /api/v1/health`
- `GET /api/v1/readiness`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /docs`

The local demo identity defaults to `admin@sentinelai.example` / `change-me`. Change both values outside local development.

## Neo4j Graph Projection

Neo4j is a derived relationship store; PostgreSQL remains authoritative. Configure `NEO4J_URI`, `NEO4J_USER`, and `NEO4J_PASSWORD` to enable graph access. Without Neo4j, graph endpoints return `unavailable` and the agent workflow remains completed with an explicit graph status.

- `GET /api/v1/graph/status`
- `POST /api/v1/graph/incidents/{incident_id}/project`
- `GET /api/v1/graph/incidents/{incident_id}/context`

Docker Compose starts Neo4j at `http://localhost:7474` and Bolt at `neo4j://localhost:7687`.

## Migrations

```powershell
alembic upgrade head
```

The application currently creates the identity tables on startup for a frictionless local foundation. Migrations are the intended source of truth before production deployment.