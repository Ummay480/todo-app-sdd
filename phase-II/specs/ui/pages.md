# Application Pages (Phase II)

## Routes

### 1. Home / Dashboard (`/`)
- **Protection**: Protected Route (Redirect to `/login` if not authenticated).
- **Features**:
  - Task creation input at the top.
  - Filter tabs: All, Pending, Completed.
  - Vertical list of tasks.
  - "No tasks found" state.

### 2. Login Page (`/login`)
- **Protection**: Public (Redirect to `/` if already authenticated).
- **Features**: Simple login card, link to signup.

### 3. Signup Page (`/signup`)
- **Protection**: Public.
- **Features**: Registration card, link to login.

## Middleware logic
- Check JWT session on every page request.
- Handle redirects for protected vs public routes.

## Performance
- Next.js Server Components for initial load.
- Optimistic UI updates for task completion and deletion.
