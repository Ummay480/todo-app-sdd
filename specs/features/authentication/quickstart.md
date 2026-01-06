# Quickstart: Authentication Setup

This document outlines the steps to verify and set up the Authentication system for Phase-II.

## Frontend Setup (Next.js)

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install better-auth
   ```

2. **Environment Variables**:
   Create or update `frontend/.env.local`:
   ```env
   BETTER_AUTH_SECRET=your_generated_secret
   BETTER_AUTH_URL=http://localhost:3000
   ```

3. **Verify Auth Client**:
   Ensure `frontend/src/lib/auth-client.ts` is configured with the JWT plugin:
   ```typescript
   import { createAuthClient } from "better-auth/react";
   import { jwtClient } from "better-auth/client/plugins";

   export const authClient = createAuthClient({
     plugins: [jwtClient()]
   });
   ```

## Backend Setup (FastAPI)

1. **Install Dependencies**:
   ```bash
   cd backend
   pip install "python-jose[cryptography]" httpx
   ```

2. **Verify Middleware**:
   Ensure `backend/src/auth/jwt_middleware.py` (to be created) correctly fetches the JWKS from `http://localhost:3000/api/auth/jwks`.

## Manual Verification Scan
1. Navigate to `/signup` and create an account.
2. Check `localStorage` or cookies to verify the session.
3. Call a protected FastAPI endpoint using the JWT in the header.
