# Database Schema (Phase II)

## Database Engine
Neon Serverless PostgreSQL

## ORM
SQLModel (Python)

## Tables

### Users (Internal/Auth)
Managed by Better Auth.
- `id`: UUID (Primary Key)
- `email`: String (Unique)
- `name`: String
- `hashed_password`: String (if applicable)

### Tasks
- `id`: UUID (Primary Key, default uuid7)
- `user_id`: UUID (Foreign Key -> Users.id)
- `title`: String (Required, 1-100 characters)
- `description`: String (Optional)
- `is_completed`: Boolean (Default: False)
- `priority`: Enum (Low, Medium, High; Default: Medium)
- `created_at`: DateTime (Auto)
- `updated_at`: DateTime (Auto)

## Constraints
1. **User Isolation**: All queries on `Tasks` MUST include `WHERE user_id = :current_user_id`.
2. **Index**: Composite index on `(user_id, created_at)` for efficient listing.
3. **Validation**: Titles cannot be empty or solely whitespace.
