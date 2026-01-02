---
id: 011
title: troubleshoot frontend module error
stage: misc
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: Phase-1
user: unknown
command: cd phase-II/frontend && npm install
labels: ["frontend", "nextjs", "npm-error", "sonner"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - none
tests:
  - npm run dev (failed with Module Not Found)
  - npm install (in progress via background shell)
---

## Prompt

./node_modules/next/dist/pages/_app.js:14:16
Module not found: Can't resolve '../shared/lib/utils'

## Response snapshot

Identified missing `sonner` dependency and possible `node_modules` corruption. Initiated a clean install in the background.

## Outcome

- ✅ Impact: Troubleshooting path established; clean install requested.
- 🧪 Tests: Monitored background install; identified `sonner` as a missing top-level dependency in `layout.tsx`.
- 📁 Files: None (package.json not yet updated as install is running).
- 🔁 Next prompts: Wait for clean install to complete and verify `localhost:3000`.
- 🧠 Reflection: Next.js 15+ can have flaky `node_modules` if interrupted or if `swc` binaries fail to download properly.

## Evaluation notes (flywheel)

- Failure modes observed: `npm error ENOTEMPTY: directory not empty, rename` during repair.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Check if `sonner` needs to be added to `package.json` explicitly.
