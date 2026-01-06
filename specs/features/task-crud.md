# Feature Specification: Task CRUD and Intermediate Features

**Feature Branch**: `task-crud-implementation`
**Created**: 2026-01-02
**Status**: Draft
**Input**: Comprehensive task management including multi-user isolation, CRUD operations, priority, search, filtering, and sorting.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-User Task Isolation (Priority: P1)
As a logged-in user, I want to see only my own tasks so that my data remains private and isolated from other users.

**Why this priority**: Fundamental requirement for the multi-user nature of the application.
**Independent Test**: Create two different users, add tasks to each, and verify that neither user can see or modify the other's tasks via the UI or API.

**Acceptance Scenarios**:
1. **Given** I am logged in as User A, **When** I view my task list, **Then** I only see tasks I created.
2. **Given** I know the ID of User B's task, **When** I attempt to fetch or update it via API, **Then** the system returns a 404 or 403 error.

---

### User Story 2 - Task Lifecycle Management (Priority: P1)
As a user, I want to create, view, toggle completion, and delete tasks so that I can manage my daily work effectively.

**Why this priority**: Core CRUD functionality required for any task application.
**Independent Test**: Perform a full cycle of creating a task, viewing it in the list, marking it as complete, and then deleting it.

**Acceptance Scenarios**:
1. **Given** I am on the dashboard, **When** I enter "Buy milk" and click "Add", **Then** the task appears in my list with a "pending" status.
2. **Given** a task "Buy milk", **When** I click its checkbox, **Then** its status toggles to "completed" and it is visually updated.
3. **Given** a task "Buy milk", **When** I click the "Delete" icon, **Then** the task is removed from the list and the database.

---

### User Story 3 - Prioritization (Priority: P2)
As a user, I want to assign a priority (High, Medium, Low) to my tasks so that I can focus on the most important ones.

**Why this priority**: Intermediate feature to help users organize work by importance.
**Independent Test**: Create tasks with different priority levels and verify they are stored and displayed correctly.

**Acceptance Scenarios**:
1. **Given** I am creating a task, **When** I select "High" priority, **Then** the task is saved with that priority level.
2. **Given** an existing task, **When** I change its priority from "Medium" to "Low", **Then** the change is persisted.

---

### User Story 4 - Search, Filter, and Sort (Priority: P2)
As a user with many tasks, I want to search by title, filter by status, and sort by date or priority so that I can find specific tasks quickly.

**Why this priority**: Essential for usability when the number of tasks grows.
**Independent Test**: Use search, filter, and sort controls and verify the displayed list matches the criteria.

**Acceptance Scenarios**:
1. **Given** tasks named "Buy milk" and "Read book", **When** I search for "milk", **Then** only "Buy milk" is displayed.
2. **Given** mixed completed and pending tasks, **When** I filter for "Completed", **Then** only completed tasks are shown.
3. **Given** tasks with different priorities, **When** I sort by "Priority (High to Low)", **Then** High priority tasks appear at the top.

---

### Edge Cases
- **Unauthenticated Access**: Attempting to access task endpoints without a valid JWT should return 401 Unauthorized.
- **Empty State**: When a user has no tasks, the UI should show a friendly "No tasks found" message rather than a blank screen.
- **Searching Empty Results**: Searching for a term that matches nothing should show "No tasks matching your search."
- **Long Titles**: Titles up to 100 characters must be supported; longer ones should be truncated or rejected.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001 (Isolation)**: Every task MUST be associated with a `user_id` and all backend queries MUST filter by the current user's ID.
- **FR-002 (Create)**: System MUST allow creating a task with a title (required), description (optional), and priority (default: Medium).
- **FR-003 (Read)**: System MUST provide an endpoint to list tasks for the current user, supporting filtering (by status) and sorting (by date and priority).
- **FR-004 (Update)**: System MUST allow updating a task's title, description, status, and priority.
- **FR-005 (Delete)**: System MUST allow permanent deletion of a task.
- **FR-006 (Search)**: System MUST support server-side search by title (case-insensitive partial matches).

### Technical Requirements
- **Backend (FastAPI)**:
  - Implement GET, POST, PUT, DELETE endpoints under `/api/tasks`.
  - Use `Depends(get_current_user)` to enforce authentication and retrieve `user_id`.
  - Use SQLModel for database interactions with Neon PostgreSQL.
- **Frontend (Next.js)**:
  - Use React Query (or similar) for data fetching and optimistic updates.
  - Implement a responsive UI with Tailwind CSS.
  - Display "Empty State" illustrations or messages when appropriate.

### Key Entities
- **Task**:
    - `id`: UUID (Primary Key)
    - `user_id`: UUID (Foreign Key)
    - `title`: String (1-100 chars)
    - `description`: String (Optional)
    - `is_completed`: Boolean
    - `priority`: Enum (Low, Medium, High)
    - `created_at`: DateTime
    - `updated_at`: DateTime

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: 100% of API requests for tasks are authorized via JWT.
- **SC-002**: Unauthorized users are unable to access tasks of other users (0 leaks in testing).
- **SC-003**: UI reflects database changes (CRUD) within 200ms of server confirmation.
- **SC-004**: Search and Filter operations complete in under 100ms for lists up to 500 tasks.
- **SC-005**: 100% coverage for Task CRUD logic in backend unit tests.
