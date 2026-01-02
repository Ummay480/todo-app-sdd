# Backend Guidelines (Phase II - Follow-on)

## Stack
- Python 3.12+
- FastAPI
- SQLModel (ORM)
- Pydantic v2
- Neon PostgreSQL (Driver: `psycopg2-binary` or `asyncpg`)

## Auth Integration
- Shared secret `BETTER_AUTH_SECRET` for JWT verification.
- Middleware to inject `current_user` into request state.

## Patterns
- Dependency Injection for DB sessions and Auth.
- Pydantic schemas for Request/Response validation.
- Row Level Security: Every query must filter by `owner_id`.

## Commands
- `uvicorn main:app --reload`: Start development server.
- `pytest`: Run backend suite.
