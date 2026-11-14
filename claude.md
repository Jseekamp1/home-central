# Home Central

A home project planner. Homeowners capture, plan, schedule, and track maintenance and improvement projects in one place: AI-assisted project planning, materials and shopping lists, recurring maintenance tailored to their home, and a scheduler that fits work into their available time by priority, duration, and materials on hand.

The roadmap is in [roadmap.md](roadmap.md). Each milestone's decisions live in `specs/milestone-N.md`.

## Tech Stack

- **Backend**: Python, FastAPI, SQLModel, Alembic migrations, SQLite for local development. The production database is decided in Milestone 10. Keep the schema Postgres-compatible: no SQLite-only types or behavior.
- **Frontend**: Nuxt 4 (Vue 3), TypeScript strict, Tailwind CSS. Use shadcn-vue for UI primitives; install it when the first component needs one.
- **AI**: LLM calls happen only in the backend. Mock the LLM in tests, never the database.
- **Auth**: Until a real auth provider is chosen, `get_current_user` (backend shared dependency) returns a fixed dev user. All data access goes through it, so swapping in real auth touches one place.

## Mobile Portability

Mobile comes later and does not need to share code with the web app, so the web app must stay a thin client of the API:

- The backend API is the product. Every feature works through documented REST endpoints, so any client (web, PWA, Capacitor, native iOS) can use it.
- The frontend uses no server-side Nuxt features (server routes, SSR-only data loading). It must work as a static SPA.
- Auth uses bearer tokens, not cookies.
- Mobile-first layouts: design for small screens, then add breakpoints.

## Architecture

**Vertical slices.** Code is organized by feature, not by layer. `backend/app/features/<feature>/` holds that feature's router, models, service, and tests. `frontend/app/features/<feature>/` mirrors it by name with components, composables, and tests. Shared code goes in `shared/` only once the same logic appears in 3+ features; some duplication is preferred over a wrong abstraction.

**Layer responsibilities.**
- The backend owns business logic: calculations, validation, scheduling rules, cost aggregation, recurrence, and all database access.
- The frontend fetches data, displays it, collects input, and sends it to the API. Logic beyond UI state (toggles, local filtering, form validation) belongs in a backend endpoint.

**Types.** The backend SQLModel models are the single source of truth. Frontend API types are generated from the backend's OpenAPI schema, never handwritten, so the two sides cannot drift.

**Patterns.** Once a pattern exists (errors, validation, response shapes, auth), follow it. Propose changes to established patterns; don't change them unilaterally.

## Workflow

1. **Milestone planning.** Each milestone starts with a planning session, not code: ask clarifying questions, surface edge cases, and record decisions in `specs/milestone-N.md`. No implementation until the spec is approved.
2. **Plan each slice.** Before coding, read the spec and one reference feature, then present a short plan (files, data flow, tests) and wait for approval.
3. **Backend slice, then frontend slice**, as separate passes. Each is a commit checkpoint: when tests pass, say so and suggest a commit message.
4. **Ask before** adding dependencies, making architectural changes that affect multiple features, or creating files outside the established structure.

## Testing

- **TDD.** Write tests first, run them, and show they fail (red). Then implement until they pass (green). Never edit a test to make it pass; fix the implementation.
- **Meaningful tests only.** Backend tests run against a real database (in-memory SQLite) through the real API. Mock only external services (LLM, email, push).
- **Prune when a feature is done.** Delete the scaffolding tests. Keep a couple of important tests per feature: the API contract, and logic that can't be checked by eye (scheduling, cost math, recurrence dates).
- While working, run only the current feature's tests. Run the full suite before committing.

## Conventions

- One responsibility per file: one router, service, or composable per file.
- Include validation and error handling from the start, not "for now".
- No `any` in TypeScript without a stated reason. No TODO comments in place of implementation.
- Accessible UI: semantic HTML, ARIA where needed, keyboard navigable.
- Build exactly what was asked. No speculative abstractions or extra features.
- Don't claim something works without running it. If you can't run it, say so.
- If a fix fails 3 times, stop and present what you've tried and the likely root cause.
