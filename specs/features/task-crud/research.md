# Task CRUD Research Findings

This document consolidates research on best practices for SQLModel, Neon Serverless PostgreSQL, FastAPI security, and advanced CRUD operations for the Todo App.

## 1. SQLModel with Neon Serverless PostgreSQL

Neon uses **PgBouncer** in **transaction mode** to manage connections efficiently in serverless environments.

### Connection Management
- **Pooled Connection String**: Use the `-pooler` suffix in your Neon connection string and connect via port **6432**.
  - Example: `postgresql://user:password@endpoint-pooler.region.aws.neon.tech/dbname`
- **Session Lifecycle**: In FastAPI, ensure the database session is closed after each request to return the connection to the pool.
- **SQLAlchemy Engine Settings**:
  - `pool_pre_ping=True`: Check connection health before using it.
  - `pool_size` and `max_overflow`: For serverless apps (where many small instances may run), set these to small values (e.g., `pool_size=5`, `max_overflow=10`) or use `NullPool` if the application instance is short-lived and doesn't benefit from local pooling.
  - **Note**: Since Neon manages pooling externally via PgBouncer, the client-side pool doesn't need to be large.

### Transaction Mode Caveat
Neon's PgBouncer runs in **transaction mode**. Avoid using `SET` or `RESET` commands that rely on session state, as these will not persist across transactions.

---

## 2. "Security by Design" Patterns in FastAPI

Isolating user data and ensuring unauthorized access is prevented by design.

### Dependency Injection Pattern
Extract the user ID once in a shared dependency and use it across all CRUD operations.

```python
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from app.db import get_session
from app.models import User, Task
from app.auth import get_current_user

# Global dependency to provide a "filtered" session or just the user_id
async def get_current_active_user(user: Annotated[User, Depends(get_current_user)]):
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

# Sharing user_id across dependencies
@app.get("/tasks/")
def read_tasks(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    # Security by Design: Always filter by current_user.id
    statement = select(Task).where(Task.user_id == current_user.id)
    return session.exec(statement).all()
```

### Key Principles
- **Centralized Extraction**: Extract `user_id` in a reusable dependency.
- **Mandatory Filtering**: Every query involving user-owned data MUST include a `.where(Model.user_id == current_user.id)` clause.
- **No Direct Parameter Access**: Never allow `user_id` to be passed as a query parameter or request body for CRUD operations; always derive it from the authentication token.

---

## 3. Handling Enums in SQLModel

Proper integration of Python Enums with PostgreSQL native ENUM types.

### Implementation Pattern
Use Python `Enum` and map it to `SQLAlchemy_Enum` for PostgreSQL compatibility.

```python
from enum import Enum
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Enum as SQLAlchemy_Enum

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    # Use sa_column for native PostgreSQL ENUM support
    priority: TaskPriority = Field(
        sa_column=Column(
            SQLAlchemy_Enum(TaskPriority, name="taskpriority", native_enum=True),
            nullable=False,
            server_default=TaskPriority.MEDIUM.value
        )
    )
```

- **`native_enum=True`**: Tells SQLAlchemy to use the `CREATE TYPE ... AS ENUM` command in PostgreSQL.
- **`name="taskpriority"`**: Specifies the name of the type in the database.

---

## 4. Efficient Server-Side Search and Filtering

Leveraging SQLModel's expression system for database-level operations.

### Search (LIKE / ILIKE)
Use `col().ilike()` for case-insensitive partial matches.

```python
from sqlmodel import select, col

def search_tasks(session: Session, user_id: int, query: str):
    statement = select(Task).where(
        Task.user_id == user_id,
        col(Task.title).ilike(f"%{query}%")
    )
    return session.exec(statement).all()
```

### Filtering and Pagination
Combine `offset()` and `limit()` for efficient results retrieval.

```python
@app.get("/tasks/")
def get_tasks(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    offset: int = 0,
    limit: Annotated[int, Field(le=100)] = 20,
    priority: TaskPriority | None = None
):
    statement = select(Task).where(Task.user_id == current_user.id)

    if priority:
        statement = statement.where(Task.priority == priority)

    statement = statement.offset(offset).limit(limit)
    return session.exec(statement).all()
```

### Best Practices
- **Database-Level Operations**: Always filter and paginate in the database, never in Python.
- **Method Chaining**: Use SQLModel's chainable API (`select().where().offset().limit()`).
- **Input Validation**: Use Pydantic/FastAPI constraints (like `le=100` for limit) to prevent resource exhaustion.

## Sources:
- [Neon: Connection Pooling](https://neon.com/docs/connect/connection-pooling/)
- [FastAPI: Security - Get Current User](https://fastapi.tiangolo.com/tutorial/security/get-current-user/)
- [SQLModel: Filtering with where()](https://sqlmodel.tiangolo.com/tutorial/where/)
- [SQLModel: Offset and Limit](https://sqlmodel.tiangolo.com/tutorial/offset-and-limit/)
- [SQLModel Tutorial: Enums (Implicit)](https://sqlmodel.tiangolo.com/tutorial/enums/)
- [SQLAlchemy: Enum API](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum)
