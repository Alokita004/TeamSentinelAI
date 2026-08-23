# SentinelAI Architecture Decisions

Status: Proposed baseline for approval
Date: 2026-08-20

This document records decisions that should govern future implementation. Items marked `DECISION REQUIRED` must be resolved before the relevant phase is locked.

## 1. Why Next.js

**Proposed decision:** Use Next.js with the App Router and TypeScript for the government emergency dashboard.

It provides a structured React application, route-level organization, server/client boundaries, and a mature deployment path. The dashboard should remain primarily a client-interactive operational surface while using server capabilities only where they simplify secure integration. Exact Next.js and React versions are `DECISION REQUIRED`.

## 2. Why FastAPI

**Proposed decision:** Use FastAPI as the Python API boundary.

FastAPI aligns with Pydantic validation, typed OpenAPI contracts, async I/O, SSE support, and Python's AI/data ecosystem. It should expose versioned REST endpoints and a dedicated SSE stream rather than allowing the frontend to call agents or databases directly.

## 3. Why LangGraph

**Proposed decision:** Use LangGraph for durable, observable multi-agent orchestration after deterministic domain services exist.

The graph should model execution state, agent sequencing, events, errors, and future branching. LangGraph is not the owner of persistence, authorization, routing algorithms, or provider credentials. The exact checkpoint and persistence approach is `DECISION REQUIRED`.

## 4. Why PostgreSQL

**Proposed decision:** PostgreSQL is the transactional source of truth.

It should own incidents, users, permissions, assessments, resource allocations, routes, notifications, execution records, events, and audit logs. SQLAlchemy and migrations should make schema changes repeatable. Transaction boundaries and event retention are `DECISION REQUIRED`.

## 5. Why Neo4j

**Proposed decision:** Use Neo4j for relationship-heavy intelligence and graph traversal.

It should answer questions involving connected roads, zones, shelters, hospitals, resources, teams, and incidents. Neo4j must not become a second competing transactional authority. Projection identity, freshness, rebuild behavior, and consistency guarantees are `DECISION REQUIRED`.

## 6. Why SSE

**Proposed decision:** Use Server-Sent Events for one-way backend-to-dashboard execution updates.

SSE fits ordered agent progress, risk changes, resource changes, notifications, and audit-visible events without requiring bidirectional socket semantics. The contract must define event IDs, ordering, replay via `Last-Event-ID`, heartbeat behavior, reconnect behavior, authorization, and stream isolation. These details are `DECISION REQUIRED`.

## 7. Why Provider Abstractions

**Proposed decision:** Define ports/interfaces for weather, traffic, river sensors, government alerts, citizen reports, historical data, remote sensing, and IoT sources.

Each provider needs a deterministic Demo implementation and a Real implementation behind the same application-facing interface. Provider failures should become typed availability/error states rather than being hidden. The first real providers and operational SLAs are `DECISION REQUIRED`.

## 8. Why Demo Mode

**Proposed decision:** Demo Mode is a first-class deterministic runtime profile.

It enables a complete flood-response walkthrough without credentials, external network calls, or nondeterministic model output. Seed data, incident IDs, event ordering, risk values, routes, allocations, notifications, and reset semantics must be reproducible. Demo isolation from production data and authorization behavior are `DECISION REQUIRED`.

## 9. PostgreSQL vs Neo4j Responsibilities

**Proposed decision:** PostgreSQL owns durable business truth; Neo4j owns derived relationship intelligence.

Writes that affect business state go through application services and PostgreSQL. A projection process updates Neo4j from durable events or explicit rebuild jobs. Graph results return references to PostgreSQL entities, and stale graph data is visible to callers. The projection mechanism and acceptable staleness window are `DECISION REQUIRED`.

## 10. Agent vs Service Responsibilities

**Proposed decision:** Agents coordinate reasoning and produce structured recommendations; application/domain services enforce deterministic rules and perform authorized writes.

For example, RouteAgent may request route analysis, while a route service calculates constraints and a command service persists an approved result. Agents cannot bypass authorization, call databases directly, or send unvalidated notifications. Human approval requirements for high-impact actions are `DECISION REQUIRED`.

## 11. DisasterStrategy Abstraction

**Proposed decision:** Introduce a disaster strategy port so the orchestration contract is disaster-neutral.

A strategy should provide incident normalization, hazard-specific risk inputs, impact rules, simulation data, and validation while sharing common state, agents, services, persistence, and event contracts. Flood is the first concrete strategy. Cyclone, earthquake, landslide, and wildfire remain future strategies. The exact plugin/registry API is `DECISION REQUIRED`.

## 12. Authentication Architecture

**DECISION REQUIRED.** The product needs identity, roles, authorization scopes, session/token expiry, emergency overrides, and auditability. A practical initial choice is a backend-controlled secure session or OIDC-backed identity with FastAPI authorization checks and role/scope claims. The identity provider, deployment model, MFA requirement, and demo login policy must be approved before Phase 2 is complete.

## 13. Frontend State Architecture

**Proposed decision:** Use Zustand for cross-page operational state, local component state for ephemeral UI state, React Hook Form plus Zod for forms, and typed API/SSE adapters for server state updates.

Incident, dashboard snapshot, agent execution, map layers, resources, notifications, and connection status should have explicit ownership. The store should not duplicate every server entity without reconciliation rules. Cache/query library selection, if any, is `DECISION REQUIRED`.

## 14. Production/AWS Separation from Local Demo

**Proposed decision:** Keep local Demo Mode runnable with Docker Compose and no AWS dependency. Treat AWS as a deployment target, not an application assumption.

Production may use CloudFront, S3, API Gateway, ECS/Fargate, Lambda, EventBridge, RDS PostgreSQL, ElastiCache Redis, CloudWatch, and Secrets Manager, but each is P2 until the local P0 flow works. The final AWS topology, networking, IAM, and cost controls are `DECISION REQUIRED`.

## Cross-Cutting Rules

- Use typed contracts at frontend/API, API/service, agent/state, and provider boundaries.
- Preserve correlation IDs across requests, agent executions, events, and audit records.
- Make external calls observable, timeout-bounded, and replaceable.
- Prefer idempotent commands for simulation, reset, allocation, and notification actions.
- Keep P0 work ahead of assistant, multilingual, satellite, IoT, and AWS features.
