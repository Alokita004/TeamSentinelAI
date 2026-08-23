# SentinelAI Implementation Plan

Date: 2026-08-20
Planning basis: empty repository audit; all implementation status is currently NOT VERIFIED.

## Dependency Structure

The requested order is a sound critical path because each later phase consumes contracts or data established earlier:

```text
Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6
                                               |
                                               v
                                      Phase 7 -> Phase 8 -> Phase 9 -> Phase 10
```

Phase 7 depends on Phase 4 and the Phase 2 API foundation. Phase 8 depends on the services created in Phases 3, 5, and 6. Phase 9 hardens all previous slices. Phase 10 is the release gate. Provider interfaces, shared types, event envelopes, and disaster strategy boundaries should be designed in Phase 2/3, but their full implementations must stay in their assigned phases.

## Phase 1 - UI Foundation

### Objective
Create the responsive SentinelAI operational dashboard shell without real backend functionality.

### Dependencies
Repository-local Git boundary and an approved frontend package/version set. No backend dependency; use typed fixtures.

### Frontend Changes
Create Next.js App Router TypeScript structure, Tailwind and shadcn/ui foundations, design tokens, responsive sidebar/header, dashboard shell, KPI cards, map shell, agent pipeline, recommendation panel, incident timeline, and mobile layout. Add Lucide icons, Framer Motion transitions, React Leaflet/Recharts placeholders only where useful, and Zustand fixture state.

### Backend Changes
None. Define frontend mock adapters only; do not create the backend yet.

### Database Changes
None.

### Neo4j Changes
None.

### API Changes
Document the future dashboard snapshot, simulation command, reset command, and SSE event shapes as frontend types or contract notes. Do not expose a real API.

### Infrastructure Changes
Add frontend-local scripts/configuration only. Avoid databases and unnecessary services.

### Tests
Component tests for key states, responsive smoke checks, and accessibility checks for navigation and controls.

### Verification
Run install-free checks only if tooling exists; otherwise verify with the chosen frontend build and focused tests after dependencies are intentionally installed.

### Definition of Done
The dashboard shell renders on desktop/mobile with deterministic fixtures, no real backend claims, and stable loading/empty/error states.

### Risks
Premature visual coupling to backend models; map/chart dependencies; unclear responsive behavior.

### Expected Files
`frontend/` or approved root Next.js structure, `package.json`, Tailwind/shadcn configuration, app routes, components, stores, fixtures, and frontend tests.

## Phase 2 - Backend Foundation

### Objective
Establish a secure, typed FastAPI service and PostgreSQL foundation.

### Dependencies
Phase 1 contracts and approved decisions for authentication and repository layout.

### Frontend Changes
Replace mock API boundary with typed REST client scaffolding; retain mock mode behind configuration.

### Backend Changes
Create FastAPI app, configuration/environment validation, versioned routes, Pydantic schemas, SQLAlchemy models/session, repositories, services, structured errors, request IDs, health/readiness endpoints, and initial authentication/authorization middleware.

### Database Changes
Create PostgreSQL Compose service only if needed, migration framework, initial users/roles schema, and transaction conventions.

### Neo4j Changes
None.

### API Changes
Define `/api/v1/health`, readiness, auth/session endpoints, and stable error/envelope conventions. Reserve incident, simulation, dashboard, and SSE routes.

### Infrastructure Changes
Add Python dependency files, Dockerfile/Compose for API and PostgreSQL, environment example, and local startup documentation. Do not add AWS resources.

### Tests
Schema, repository, service, auth, permission, health, error, and migration tests.

### Verification
Migrations apply from empty database; API starts; readiness reflects dependencies; unauthorized requests are rejected.

### Definition of Done
A reproducible API/database foundation exists with no disaster logic.

### Risks
Overbuilding identity; insecure defaults; migration drift.

### Expected Files
`backend/`, dependency/lock files, migrations, Docker files, `.env.example`, API tests, and configuration docs.

## Phase 3 - Demo Data + Flood Simulation

### Objective
Deliver deterministic urban flood incident creation and reset.

### Dependencies
Phase 2 persistence, auth policy, API error contracts, and provider ports.

### Frontend Changes
Wire simulate/reset controls to commands and render initial incident state.

### Backend Changes
Add `FloodStrategy`, incident lifecycle, deterministic seed script, Demo provider implementations, simulation command, reset command, and idempotency rules.

### Database Changes
Add incidents, affected zones, citizens/reports, shelters, hospitals, ambulances, rescue teams, resources, and seed metadata as needed for the P0 flow.

### Neo4j Changes
None; produce graph projection input records only.

### API Changes
Add authenticated simulation/reset and dashboard snapshot endpoints with explicit demo-mode guardrails.

### Infrastructure Changes
Add repeatable seed/reset commands and optional local service wiring.

### Tests
Fixture determinism, simulation idempotency, reset isolation, strategy validation, and API integration tests.

### Verification
Fresh setup produces the same incident IDs/data and reset restores the initial state.

### Definition of Done
The full flood fixture exists without real providers or LLM dependence.

### Risks
Non-idempotent reset, data leakage between demo users, hidden randomness.

### Expected Files
Flood strategy, provider ports/adapters, seed data, simulation service, lifecycle routes, and tests.

## Phase 4 - LangGraph

### Objective
Orchestrate the typed disaster workflow and record structured execution events.

### Dependencies
Phase 3 incident data and Phase 2 service boundaries.

### Frontend Changes
Render agent statuses from fixture/API execution records; no live stream requirement yet.

### Backend Changes
Define `DisasterState`, agent event/error models, graph builder, and Alert, Risk, Impact, Graph, Route, Resource, Decision, and Notification agents. Agents call services and providers through interfaces.

### Database Changes
Add agent executions, agent events, recommendations, and execution status persistence.

### Neo4j Changes
Define graph context interface only; use a demo context provider until Phase 5.

### API Changes
Add simulation execution status and recommendation endpoints; preserve structured event ordering.

### Infrastructure Changes
No new production infrastructure. Set execution timeouts and bounded concurrency.

### Tests
State transitions, agent contracts, failure propagation, retries/idempotency, and deterministic end-to-end graph tests.

### Verification
One simulation completes in the specified order and records every agent event, recommendation, and error.

### Definition of Done
The graph drives a repeatable flood workflow with typed outputs and no direct database bypasses.

### Risks
Agent nondeterminism, runaway retries, unclear human approval boundaries.

### Expected Files
Agent package, graph/orchestration package, state schemas, execution services, and tests.

## Phase 5 - Neo4j

### Objective
Add relationship intelligence without moving transactional ownership out of PostgreSQL.

### Dependencies
Phase 4 graph context contract and Phase 3 stable entity identifiers.

### Frontend Changes
Add knowledge graph data adapter and initial graph context view when backend data is available.

### Backend Changes
Create Neo4j connection/configuration, repository, Cypher modules, projection/rebuild process, and GraphAgent integration.

### Database Changes
Add projection version/status metadata in PostgreSQL if needed.

### Neo4j Changes
Create constraints/indexes, node/relationship schema, seed data, and queries for zones, roads, shelters, hospitals, teams, resources, and incidents.

### API Changes
Expose graph context/query endpoints with freshness metadata and authorization.

### Infrastructure Changes
Add Neo4j to local Compose only for this phase; document resource requirements and health checks.

### Tests
Cypher/repository integration tests, projection consistency, rebuild, stale data, and GraphAgent tests.

### Verification
A clean graph can be seeded/rebuilt and returns expected flood relationships using PostgreSQL IDs.

### Definition of Done
Graph reasoning works as a derived intelligence capability and survives rebuild.

### Risks
Dual-write inconsistency, expensive traversals, graph schema drift.

### Expected Files
Neo4j repository, Cypher/schema scripts, projection jobs, Compose updates, and tests.

## Phase 6 - Evacuation + Resources

### Objective
Calculate safe evacuation routes and allocate scarce resources.

### Dependencies
Phase 3 flood data, Phase 5 graph queries, and Phase 4 agent contracts.

### Frontend Changes
Add route layers, blocked-route states, shelter capacity, resources, and decision panels.

### Backend Changes
Implement route engine, route ranking, blocked-route handling, shelter capacity checks, resource allocation, and decision services with explicit constraints.

### Database Changes
Add/complete evacuation routes, resource allocations, capacity snapshots, and decision records.

### Neo4j Changes
Add route and proximity traversals needed by the route/resource services.

### API Changes
Expose route, shelter, resource, allocation, and decision results with idempotent commands.

### Infrastructure Changes
No new production platform; add only required deterministic route fixtures.

### Tests
Route safety/ranking, blocked roads, capacity, allocation conflicts, authorization, and integration tests.

### Verification
The demo produces ranked safe routes and explainable allocations under constrained capacity.

### Definition of Done
P0 evacuation/resource/decision behavior is deterministic, persisted, and visible through APIs.

### Risks
Unsafe recommendations, stale capacity, geographic assumptions.

### Expected Files
Route/resource/decision services, schemas, repositories, agent adapters, map adapters, and tests.

## Phase 7 - Real-Time Visualization

### Objective
Stream execution and operational updates to the dashboard.

### Dependencies
Phase 2 API/auth, Phase 4 events, and Phase 6 result models.

### Frontend Changes
Implement SSE client, reconnect/status handling, live pipeline, timeline, map, risk, resource, and notification updates.

### Backend Changes
Implement authorized SSE broker/stream, event serialization, replay/ordering, heartbeat, and execution isolation.

### Database Changes
Use persisted event history for replay/audit as designed.

### Neo4j Changes
None beyond emitting graph result events.

### API Changes
Finalize SSE endpoint and event envelope; support `Last-Event-ID` or document an approved alternative.

### Infrastructure Changes
Configure proxy buffering/timeouts for SSE locally and in deployment documentation.

### Tests
Event ordering, reconnect/replay, disconnect, authorization, load, and browser integration tests.

### Verification
A simulation updates all dashboard surfaces in order without refresh and recovers from reconnect.

### Definition of Done
Live visualization is reliable and traceable to persisted execution events.

### Risks
Dropped events, proxy buffering, duplicate application of updates.

### Expected Files
SSE transport, event store/broker, frontend stream store, live components, and tests.

## Phase 8 - AI Assistant

### Objective
Provide an English-first emergency assistant using bounded backend tools.

### Dependencies
Stable risk, shelter, route, resource, auth, and audit APIs from Phases 2-7.

### Frontend Changes
Add assistant UI, loading/error states, citations/context references, and emergency escalation affordances.

### Backend Changes
Add assistant API, intent handling, tool registry, risk/shelter/route/resource lookup, response policy, timeouts, and audit records.

### Database Changes
Persist assistant sessions/messages only if approved; retain tool/audit references.

### Neo4j Changes
Allow graph lookup through controlled tools, not direct model access.

### API Changes
Add authenticated assistant endpoint/stream and typed tool/result contracts.

### Infrastructure Changes
Configure model/provider settings through secrets and add demo deterministic responses.

### Tests
Tool authorization, prompt/input limits, deterministic demo responses, refusal/error paths, and end-to-end questions.

### Verification
Representative emergency questions return current, source-linked operational answers without unauthorized actions.

### Definition of Done
Assistant is useful, bounded, auditable, and English-first with a multilingual extension point.

### Risks
Hallucination, stale data, prompt injection, latency, and cost.

### Expected Files
Assistant routes/services/tools, policies, frontend components, model adapters, and tests.

## Phase 9 - Production Hardening

### Objective
Raise the working P0/P1 system to a defensible production baseline.

### Dependencies
All prior runtime paths and approved security decisions.

### Frontend Changes
Harden auth/session handling, error boundaries, input limits, accessibility, offline/demo indicators, and telemetry hooks.

### Backend Changes
Harden authorization, audit logging, structured logging, request IDs, rate limits, security headers, input limits, retries, timeouts, and environment validation.

### Database Changes
Review indexes, retention, backups, least-privilege roles, migration rollback strategy, and audit immutability.

### Neo4j Changes
Review credentials, least privilege, indexes, query limits, backup/rebuild, and projection monitoring.

### API Changes
Finalize OpenAPI, versioning, error taxonomy, health/readiness, rate-limit responses, and security policy.

### Infrastructure Changes
Harden images/Compose, CI/CD, secret handling, observability, and only then design AWS deployment components.

### Tests
Security, integration, contract, migration, load, accessibility, dependency scanning, and CI checks.

### Verification
Repeatable CI passes, secrets are externalized, services fail safely, and operational runbooks exist.

### Definition of Done
P0/P1 is deployable with documented controls and known residual risks.

### Risks
Scope expansion, cloud cost, false confidence from shallow security tests.

### Expected Files
CI workflows, Docker hardening, security/config modules, runbooks, and expanded tests.

## Phase 10 - Final E2E Verification

### Objective
Verify the complete deterministic user journey and release readiness.

### Dependencies
Phases 1-9 complete and all DECISION REQUIRED items resolved.

### Frontend Changes
Fix only issues discovered by E2E verification; capture desktop/mobile evidence.

### Backend Changes
Fix only workflow defects; freeze public contracts after sign-off.

### Database Changes
Run clean migration/seed/reset and verify audit/event persistence.

### Neo4j Changes
Run clean schema/seed/rebuild and verify GraphAgent results.

### API Changes
Verify auth, simulation, agents, results, SSE, assistant, audit, and reset contracts.

### Infrastructure Changes
Verify local Compose and approved deployment checks; AWS remains optional unless explicitly in scope.

### Tests
Full browser E2E: Login -> Dashboard -> Flood Simulation -> Agents -> Neo4j -> Risk -> Evacuation -> Resources -> Decision -> Notifications -> SSE -> Assistant -> Audit -> Reset.

### Verification
Run from a clean environment and repeat reset/simulation to confirm deterministic behavior, authorization, event ordering, and no data leakage.

### Definition of Done
The complete acceptance path passes, evidence is recorded, and remaining risks are explicitly accepted.

### Risks
Environment-specific failures, flaky timing, external service availability.

### Expected Files
E2E specs, test fixtures, release checklist, and verification report.
