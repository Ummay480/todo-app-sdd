# Better Auth in Next.js 15 App Router - Implementation Research

## Overview
Better Auth is the selected authentication framework. This document synthesizes best practices for integrating it with Next.js 15 (App Router).

## 1. Setting Up auth-client.ts
- **Path**: `/phase-II/frontend/src/lib/auth-client.ts`
- **Pattern**: `createAuthClient` with `baseURL` from env.
- **Note**: Ensure `credentials: "include"` is set if cross-origin.

## 2. Middleware Implementation
- **Path**: `/phase-II/frontend/src/middleware.ts`
- **Pattern**: Use `betterFetch` to check session on protected routes.
- **Redirects**: Unauthenticated users on `/` -> `/login`.

## 3. Secret Management
- **Key**: `BETTER_AUTH_SECRET` (min 32 chars).
- **Environment**: Shared between Frontend (Better Auth) and Backend (FastAPI).
- **Deployment**: Must be set via environment variables, never committed.

## 4. Session Checking
- **Server-Side**: `getSession()` in `layout.tsx` for initial redirect/auth state.
- **Client-Side**: `useSession()` for UI components like navigation and user profiles.

## 5. Error Handling
- Map Better Auth error codes (e.g., `EMAIL_ALREADY_EXISTS`) to user-friendly messages.
- Use `zod` for client-side form validation before calling auth-client.
