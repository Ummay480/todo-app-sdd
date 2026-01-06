# Data Model: Task CRUD

## Entities

### Task
The core entity for managing todo items.
- `id`: string (UUID) - Primary Key, generated on creation.
- `user_id`: string (UUID) - Owner of the task (Foreign Key to User).
- `title`: string (1-100 characters) - The task title.
- `description`: string (optional) - Additional details.
- `is_completed`: boolean - Completion status (default: false).
- `priority`: Enum (Low, Medium, High) - Task priority level (default: Medium).
- `created_at`: datetime - Timestamp of creation.
- `updated_at`: datetime - Timestamp of last modification.

## Validation Rules
1. **Title**: Must be non-empty and between 1-100 characters.
2. **User Isolation**: The `user_id` MUST be set from the authenticated user context and never accepted directly from a client-provided body for creation/update.
3. **Priority**: Must be one of the defined Enum values.

## State Transitions
- **Create**: Initial status is usually `is_completed=false`.
- **Toggle**: Can move freely between `is_completed=true` and `false`.
- **Delete**: Permanent removal from the system.
