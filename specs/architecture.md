# Architecture Specification (Phase II)

## System Overview
A Full-Stack multi-user web application using a modern distributed architecture.

## Tech Stack
- **Frontend**: Next.js 15+ (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python), SQLModel (ORM)
- **Database**: Neon (Serverless PostgreSQL)
- **Auth**: Better Auth with JWT + SQLite (Auth primary) / PostgreSQL (App primary)

## Data Flow
1. **Frontend** (Next.js) requests data from **Backend** (FastAPI) via HTTP REST.
2. **Backend** validates the **JWT** token from the `Authorization: Bearer` header.
3. **Backend** uses **SQLModel** to query **Neon PostgreSQL**.
4. Every query MUST include a filter on `user_id` to ensure isolation.
5. **Backend** returns JSON response to **Frontend**.

## Security Model
- **Authentication**: Handled by Better Auth integration.
- **Authorization**: Token-based (JWT) transmitted via secure headers.
- **Data Isolation**: Application-level enforcement (Tenant filtering by `user_id`).

## Deployment
- **Local**: Docker Compose (services for frontend, backend).
- **Cloud**: DigitalOcean Kubernetes (Phase IV/V).
