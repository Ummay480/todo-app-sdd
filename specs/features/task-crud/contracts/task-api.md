# API Contract: Task CRUD

## Base Path
`/api/tasks` (FastAPI Backend)

## Endpoints

### GET /api/tasks
Lists tasks for the authenticated user.
- **Query Params**:
  - `status`: Optional (completed, pending)
  - `priority`: Optional (low, medium, high)
  - `search`: Optional string (title search)
  - `sort_by`: Optional (created_at, priority, title)
  - `order`: Optional (asc, desc)
- **Response (200 OK)**:
  ```json
  [
    {
      "id": "uuid",
      "title": "Task title",
      "description": "Task description",
      "is_completed": false,
      "priority": "medium",
      "created_at": "..."
    }
  ]
  ```

### POST /api/tasks
Creates a new task.
- **Auth**: Required Bearer JWT.
- **Request Body**:
  ```json
  {
    "title": "Required Title",
    "description": "Optional description",
    "priority": "medium"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": "uuid",
    "title": "Required Title",
    "is_completed": false,
    "..."
  }
  ```

### PUT /api/tasks/{id}
Updates an existing task.
- **Path Param**: `id` (UUID)
- **Request Body**: Partial or full update of title, description, is_completed, priority.
- **Response (200 OK)**: Updated task object.

### DELETE /api/tasks/{id}
Deletes a task.
- **Path Param**: `id` (UUID)
- **Response (204 No Content)**
