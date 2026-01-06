# Tasks: Authentication UI

**Input**: Design documents from `specs/features/authentication/`
**Prerequisites**: plan.md, authentication.md (spec), research.md, data-model.md, contracts/auth-api.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend structure in `backend/src/auth/` and `backend/src/api/`
- [ ] T002 Install frontend dependencies: `npm install better-auth` in `frontend/`
- [ ] T003 [P] Configure environment variables in `frontend/.env.local`
- [ ] T004 [P] Install backend security dependencies: `pip install "python-jose[cryptography]" httpx`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for authentication

- [ ] T005 Initialize Better Auth client in `frontend/src/lib/auth-client.ts` with JWT plugin
- [ ] T006 [P] Implement JWT public key (JWKS) fetching utility in `backend/src/auth/jwks.py`
- [ ] T007 [P] Create JWT validation middleware placeholder in `backend/src/auth/jwt_handler.py`
- [ ] T008 Setup route protection middleware in `frontend/src/middleware.ts`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Signup (Priority: P1) 🎯 MVP

**Goal**: Allow new users to create accounts

- [ ] T009 [US1] Create Signup form component in `frontend/src/components/auth/SignupForm.tsx`
- [ ] T010 [US1] Implement signup page at `frontend/src/app/(auth)/signup/page.tsx`
- [ ] T011 [US1] Integrate `authClient.signUp` in the signup form
- [ ] T012 [US1] Add form validation for email format and 8-character password

**Checkpoint**: User Signup functional and testable independently

---

## Phase 4: User Story 2 - User Login (Priority: P1)

**Goal**: Authenticate existing users

- [ ] T013 [US2] Create Login form component in `frontend/src/components/auth/LoginForm.tsx`
- [ ] T014 [US2] Implement login page at `frontend/src/app/(auth)/login/page.tsx`
- [ ] T015 [US2] Integrate `authClient.signIn` in the login form
- [ ] T016 [US2] Implement JWT retrieval logic for API calls in `frontend/src/lib/api-client.ts`

**Checkpoint**: User Login functional; JWTs accessible for backend requests

---

## Phase 5: User Story 3 - Logout (Priority: P2)

**Goal**: Securely sign out sessions

- [ ] T017 [US3] Create Logout button component in `frontend/src/components/auth/LogoutButton.tsx`
- [ ] T018 [US3] Integrate `authClient.signOut` with redirection to `/login`
- [ ] T019 [US2] Update dashboard layout at `frontend/src/app/(auth)/layout.tsx` to include logout

**Checkpoint**: Full auth cycle (Signup -> Login -> Logout) complete

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T020 [P] Implement global loading spinner for auth state in `frontend/src/app/providers.tsx`
- [ ] T021 [P] Ensure error messages from Better Auth are displayed via toast notifications
- [ ] T022 Document environment variable requirements in `README.md`

---

## Dependencies & Execution Order

- **Phase 1 & 2**: MUST complete before any User Story work.
- **User Story 1 (Signup)**: Independent after Phase 2.
- **User Story 2 (Login)**: Independent after Phase 2; enables real testing of US1.
- **User Story 3 (Logout)**: Depends on US2 (Login) being present.

## Implementation Strategy

1. **MVP**: Complete Signup (US1) and Login (US2) to verify JWT flow to backend.
2. **Gate**: Verify that `backend` can successfully validate a JWT from `frontend`.
