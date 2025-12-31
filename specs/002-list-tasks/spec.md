# Feature Specification: List Tasks

**Feature Branch**: `002-list-tasks`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User request: "list all tasks"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View all tasks (Priority: P1)

As a user, I want to view all my tasks so that I can see what needs to be done.

**Why this priority**: Essential for task management - users need to see their tasks.

**Independent Test**: User runs the `list` command and sees all tasks in the current session.

**Acceptance Scenarios**:

1. **Given** the storage has 3 tasks, **When** the user enters `list`, **Then** the system displays all 3 tasks with their IDs, titles, and statuses.
2. **Given** the storage is empty, **When** the user enters `list`, **Then** the system displays "No tasks found."

---

### User Story 2 - Empty list handling (Priority: P2)

As a user, I want clear feedback when I have no tasks so that I know the app is working.

**Why this priority**: Good UX - empty states should be clear.

**Independent Test**: User runs `list` on empty storage and sees friendly message.

**Acceptance Scenarios**:

1. **Given** no tasks exist, **When** the user enters `list`, **Then** the system displays "No tasks found." with helpful suggestion.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a command to list all tasks from in-memory storage.
- **FR-002**: System MUST display task ID, title, and status for each task.
- **FR-003**: System MUST handle empty list gracefully with clear message.
- **FR-004**: System MUST format output in readable table/list format.
- **FR-005**: System MUST show total task count.

### Key Entities

- **Task**: Uses existing Task TypedDict (id, title, status)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can view all tasks with 1 command.
- **SC-002**: All task fields (ID, title, status) are visible.
- **SC-003**: Empty list displays clear message.
- **SC-004**: Output is formatted and readable.
