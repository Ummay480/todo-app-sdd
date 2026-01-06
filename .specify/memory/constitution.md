<!--
Sync Impact Report - Constitution v2.2.0
========================================
Version: 2.1.0 → 2.2.0 (MINOR: Neon DB & SQLModel enforcement)
Date: 2026-01-02

Changes:
- Explicitly mandated Neon Serverless PostgreSQL and SQLModel for Phase-II.
- Strengthened User Story independence and Priority (P1/P2/P3) requirements in specifications.
- Added strict multi-user data isolation rules for database queries.

Templates Status:
- ✅ plan-template.md: Validated alignment with technical stack boundaries.
- ✅ spec-template.md: Validated alignment with prioritized user stories.
- ✅ tasks-template.md: Validated alignment with story-based task organization.

Follow-up Actions:
- Populate @specs/database/schema.md with SQLModel entity definitions.
- update @specs/architecture.md to reflect FastAPI-Neon data flow.
-->

# Todo Full-Stack Web Application Constitution (Phase II)

This Constitution defines the non-negotiable laws, constraints, and quality standards of the project.

All agents, sub-agents, skills, specifications, tasks, and implementations MUST comply with this Constitution.

**No exceptions. No overrides.**

---

## 1. Project Purpose

The goal of Phase-II is to transform the Phase-I CLI app into a modern, production-grade, multi-user Full-Stack Web Application with persistent storage.

**Priority Strategy**: Implementation will prioritize a **Frontend-First** approach, where UI/UX specifications and Frontend architecture are defined and built to drive backend requirements.

### Core Objectives

- **Spec-Driven Development (SDD)**: No code without specification.
- **Agent Orchestration**: Structured agent workflows using specialized sub-agents.
- **Reusable Intelligence**: Skills as durable, stateless units.
- **Automatic QA Enforcement**: Quality gates block progress when violated.
- **Deterministic Behavior**: Same input → same output; predictable API states.
- **Multi-User Isolation**: Every user only accesses their own data.
- **Zero Vibe-Coding**: Every decision traceable to specification or architectural record.

---

## 2. Development Philosophy (Foundation Laws)

### 2.1 Specification is the Source of Truth

**Principle**: Specifications override assumptions, preferences, and shortcuts.

**Rules**:
- No code may exist without an approved specification.
- Ambiguity MUST be resolved before planning begins.
- Incomplete specifications are invalid and MUST be rejected.
- Specifications are human-readable and machine-enforceable.

---

### 2.2 Agents, Not Prompts

**Principle**: All meaningful work MUST be executed by agents or sub-agents. Skills are reusable intelligence units.

**Rules**:
- Ad-hoc prompting is FORBIDDEN.
- Each agent has a defined scope and authority level.
- Skills are stateless, deterministic, and invoked explicitly.
- One-off instructions violate the architecture.

---

### 2.3 Quality Gate Over Speed

**Principle**: Fast but incorrect = FAILURE. Partial correctness = FAILURE.

**Rules**:
- Quality is enforced BEFORE progress is allowed.
- Failing a quality gate MUST halt execution.
- No "move fast and break things" exemptions.
- Tests (Frontend/Backend), linters, and contract checks are non-negotiable.

---

### 2.4 Security by Design

**Principle**: Authentication and Authorization are mandatory for all user interactions.

**Rules**:
- All API endpoints (except public Auth sign-in/up) MUST require a valid JWT.
- Every database query MUST filter by the authenticated user's ID.
- Tokens MUST be handled securely (Authorization: Bearer header).
- No production secrets (keys, db urls) in the codebase.

---

## 3. Phase II Technical Stack & Boundaries

### Allowed (Core Stack)

- **Frontend**: Next.js 16+ (App Router, Server Components).
- **Backend**: Python FastAPI with SQLModel ORM.
- **Auth**: Better Auth (JWT plugin enabled).
- **Database**: Neon Serverless PostgreSQL.
- **Styling**: Tailwind CSS.
- **Monorepo**: Shared specs and separate `/frontend`, `/backend` directories.

### Forbidden (Automatic Failure)

- Manual coding outside of agentic workflows.
- No-auth endpoints (except signup/signin).
- Shared sessions (cross-user data leakage).
- Hardcoded sensitive credentials.
- Bypassing the SDD workflow (e.g., skip spec for "hotfix").

---

## 4. Agent Architecture Rules

### 4.1 Main Agent (Primary Authority)

**Agent**: `todo-spec-manager`

**Responsibilities**:
- Owns the Constitution and enforces compliance.
- Approves or rejects specifications, plans, tasks, and implementations.
- Owns all architectural decisions.

---

### 4.2 Sub-Agents

**Specialized Agents**:
- `todo-domain-agent`: Business rules and logic validation.
- `python-cli-expert`: Best practices for FastAPI and Python patterns.
- `hackathon-review-agent`: Checks against hackathon judge rubrics.

---

## 5. Quality Assurance (Mandatory)

### Quality Gates

- **FAIL**: Execution MUST stop immediately.
- **PASS**: Proceed to next stage.

Quality gates checked after:
- Specification creation
- Architecture planning
- Task generation
- Implementation (Tests must pass)

---

## 6. Specification Rules

Every specification MUST include:
1. **Prioritized User Stories**: Independent P1/P2/P3 user journeys.
2. **Acceptance Criteria**: Clear, testable conditions (Given/When/Then).
3. **Edge Cases**: Auth failures, empty states, validation errors.
4. **API Contracts**: Endpoint path, method, request/response schema.
5. **Data Model**: SQLModel table definitions and relationships.
6. **UI Components**: Layout description and interactive requirements.

---

## 7. Enforced Workflow Order (Strict)

1. **Constitution**: Establish Phase II governance.
2. **Specification**: Define feature requirements (Organized by Feature/API/DB/UI).
3. **Planning**: Architecture and implementation approach (including ADRs).
4. **Task Creation**: Breakdown into testable, prioritized tasks.
5. **Implementation**: Parallel execution of frontend/backend tasks.
6. **QA Validation**: Automated tests and contract validation.

---

## 8. Error Handling Principles

- API errors MUST return standard HTTP status codes (401, 403, 404, 422, 500).
- Frontend MUST handle loading and error states gracefully with user feedback.
- No implementation details in user-facing error messages.

---

## 9. Governance

### Amendment Process
- Proposed changes MUST be documented via ADR.
- Version increment required (Semantic Versioning).
- All dependent artifacts MUST be updated for consistency.

### Versioning Policy
- **MAJOR**: Platform/Stack shift or principle removal.
- **MINOR**: New mandatory practices or feature sets.
- **PATCH**: Typos and clarifications.

---

**Version**: 2.2.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-02
