# Tasks: Task CRUD

**Input**: Design documents from `specs/features/task-crud/`
**Prerequisites**: plan.md, task-crud.md (spec), research.md, data-model.md, contracts/task-api.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend model directory in `backend/src/models/`
- [ ] T002 Create backend service directory in `backend/src/services/`
- [ ] T003 [P] Install backend dependencies: `pip install sqlmodel psycopg2-binary`
- [ ] T004 [P] Install frontend dependencies: `npm install @tanstack/react-query lucide-react`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for database and user isolation

- [ ] T005 Setup database connection and engine in `backend/src/database.py` with Neon pooling
- [ ] T006 [P] Define Priority Enum and Task model in `backend/src/models/task.py`
- [ ] T007 Implement mandatory user-filtering CRUD base in `backend/src/services/task_service.py`
- [ ] T008 [P] Configure React Query provider in `frontend/src/app/providers.tsx`

**Checkpoint**: Foundation ready - task management logic can now begin

---

## Phase 3: User Story 1 & 2 - Core CRUD & Isolation (Priority: P1) 🎯 MVP

**Goal**: Full task lifecycle with strict multi-user isolation

- [ ] T009 [US1] Implement GET `/api/tasks` with user-id filtering in `backend/src/api/tasks.py`
- [ ] T010 [US1] Implement POST `/api/tasks` with automatic user assignment in `backend/src/api/tasks.py`
- [ ] T011 [US2] Implement PUT `/api/tasks/{id}` for updates and completion toggling
- [ ] T012 [US2] Implement DELETE `/api/tasks/{id}` for task removal
- [ ] T013 [US2] Create TaskCard UI component in `frontend/src/components/tasks/TaskCard.tsx`
- [ ] T014 [US2] Create TaskList UI component in `frontend/src/components/tasks/TaskList.tsx`
- [ ] T015 [US1] Integrate `tasksApi` with React Query hooks in `frontend/src/hooks/useTasks.ts`

**Checkpoint**: Core CRUD functional with multi-user isolation verified

---

## Phase 4: User Story 3 - Prioritization (Priority: P2)

**Goal**: Support for High/Medium/Low priority levels

- [ ] T016 [US3] Add priority selector to Task creation UI in `frontend/src/components/tasks/TaskForm.tsx`
- [ ] T017 [US3] Display priority badges on `TaskCard.tsx` with color coding
- [ ] T018 [US3] Update backend service to handle priority updates in `backend/src/services/task_service.py`

---

## Phase 5: User Story 4 - Search, Filter, & Sort (Priority: P2)

**Goal**: Advanced list management for usability

- [ ] T019 [US4] Implement server-side search logic in `backend/src/services/task_service.py` using `ilike`
- [ ] T020 [US4] Create TaskFilters UI component (Search bar, Status filter, Sort dropdown)
- [ ] T021 [US4] Connect UI filters to React Query parameters in `useTasks.ts`

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T022 [P] Implement optimistic updates for task completion toggling
- [ ] T023 [P] Add loading skeletons for the task list
- [ ] T024 [P] Implement "Empty State" view when no tasks are found

## Dependencies & Execution Order

- **Phase 1 & 2**: MUST complete before any User Story work.
- **US1 & US2**: Foundation for the entire app.
- **US3 & US4**: Enhancements building on core CRUD.
