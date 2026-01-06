# Data Model: Authentication

## Entities

### User
The primary entity for authentication, managed by Better Auth.
- `id`: string (UUID) - Unique identifier for the user.
- `email`: string - User's email address (login identifier).
- `name`: string - User's display name.
- `createdAt`: datetime - Timestamp of account creation.
- `updatedAt`: datetime - Timestamp of last update.

### Session
Transient entity representing a logged-in state.
- `id`: string - Session token/identifier.
- `userId`: string - Reference to User.id.
- `expiresAt`: datetime - When the session expires.
- `token`: string (JWT) - Short-lived token for sidecar (FastAPI) requests.

## Relationships
- **User (1) <-> Session (N)**: A user can have multiple active sessions (e.g., across different devices).

## Validation Rules
1. **Email**: Must be a valid email format.
2. **Password**: Minimum 8 characters.
3. **Name**: Cannot be empty or purely whitespace.
