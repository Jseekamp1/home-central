# Home Central

## What It Does

Home Central is a home project planner that helps homeowners organize, schedule, and complete home maintenance and improvement projects. It combines project management, smart scheduling, and AI-assisted planning into a single application.

Core capabilities:

- **Project Planning** - Users describe a project (via text or speech-to-text) and the app generates materials lists, step-by-step instructions, time estimates, cost estimates, and learning resources. A conversational flow asks clarifying questions to refine details.
- **Smart Scheduling** - A calendar system that assigns projects to time slots based on priority, estimated duration, and whether the user has the required materials on hand.
- **Materials & Shopping Lists** - Tracks what materials users already own, calculates remaining costs, and builds consolidated shopping lists for upcoming projects.
- **Recurring Maintenance Reminders** - Schedules and reminds users about recurring home tasks (air filter changes, water filter replacements, appliance servicing, seasonal yard work) with advice tailored to their location and home specifications.
- **Priority Management** - Users assign priority levels to projects, and the scheduler uses these to determine what gets done first.

## What Problem It Solves

Homeowners juggle dozens of maintenance tasks and improvement projects with no unified system. They forget recurring maintenance, buy materials piecemeal, underestimate project scope, and struggle to fit projects into their available time. Home Central eliminates this by providing a single place to capture, plan, schedule, and track everything related to maintaining and improving a home.

## Tech Stack

- **Frontend**: Nuxt 3 (Vue 3), TypeScript, Tailwind CSS, shadcn-vue
- **Backend**: Python (FastAPI), Supabase (PostgreSQL, Auth, Storage)
- **AI**: LLM integration for project assistant (instructions, estimates, clarifying questions)
- **Future**: Mobile app with push notifications — build web-first with mobile portability in mind

## Milestone Planning

At the start of each milestone, the first task is always a planning session — NOT implementation. Claude should ask clarifying questions about the milestone's features, surface edge cases, and help the user work through product decisions. The output of this session is a spec file (e.g., `spec-milestone-1.md`) that captures all decisions. Do NOT begin implementation until a spec file exists and is approved for the current milestone. Planning should always use the latest **Opus** model.


# ═══════════════════════════════════════════════════════════════
# DEVELOPMENT RULES & WORKFLOW
# ═══════════════════════════════════════════════════════════════


## Project-Specific Conventions

- Build features in vertical slices — backend and frontend are implemented as SEPARATE passes, not combined into one mega-task.
- Use Vue composables for shared logic across components.
- Reusable Vue components live in a shared directory, not duplicated per feature.
- TypeScript strict mode across the frontend. No `any` types without explicit justification.
- The Supabase schema is the single source of truth for data types. Generate and share types from it. Do NOT define conflicting type definitions that drift from the schema.
- Use Row Level Security (RLS) policies for all data access control in Supabase.
- Keep API endpoints RESTful and well-documented.
- Mobile-first responsive design with Tailwind — design for small screens first, scale up.
- All UI must be accessible — semantic HTML, proper ARIA attributes, keyboard navigation.
- Follow test-driven development (TDD) — write tests first, then implement the feature to make them pass.
- Verify ALL tests pass before considering a feature complete.
- Frontend work should be completed by the **Sonnet** model.


## Workflow: Spec → Slice → Test → Commit → Repeat

IMPORTANT: Follow this sequence for every piece of work. Do not skip steps.

### 1. Read First, Code Never (Until Told)

- When given a new task, ALWAYS read the relevant files, the spec, and any reference features BEFORE proposing code.
- Present a plan and wait for approval. Do NOT jump straight to implementation.
- If the task is ambiguous, ask clarifying questions rather than guessing.

### 2. Plan Before Executing

- For any non-trivial task, create or update a brief implementation plan BEFORE writing code.
- The plan should include: which files will be created or modified, what the data flow looks like, and what tests will verify correctness.
- Keep plans concise — a short numbered list, not an essay.

### 3. One Vertical Slice at a Time

- Each task should be a single, focused feature slice — either backend OR frontend, not both at once.
- For a given feature, build the backend slice first (API route, service logic, database query, validation, tests). Get it working and committed.
- Then build the frontend slice in a separate pass (component, API call, types, tests). Get it working and committed.
- This keeps each task small enough for high-quality output within the context window.
- Do NOT implement multiple unrelated features in one pass.

### 4. Test-Driven When Possible

- Write tests FIRST based on expected input/output.
- Confirm tests fail before writing implementation.
- Do NOT modify tests to make them pass — modify the implementation instead.
- Do NOT write mock implementations for features that don't exist yet unless explicitly told to.

### 5. Commit Points

- Every completed slice (backend or frontend) should be treated as a commit checkpoint.
- When a slice is working and tests pass, say so clearly and suggest a commit message.


## Architecture Rules

### Vertical Slice Architecture

This project uses Vertical Slice Architecture. Code is organized by FEATURE, not by technical layer.

- CORRECT: `features/create-project/` contains handler, service, repository, validator, types, and tests for that feature.
- WRONG: Separate `controllers/`, `services/`, `repositories/` folders where one feature is scattered across many directories.

Backend and frontend feature folders should mirror each other by name. If the backend has `features/create-project/`, the frontend should have `features/create-project/`.

<!-- UNCOMMENT WHEN SKELETON LAYER IS ESTABLISHED
### The Skeleton Is Sacred

The skeleton (base classes, interfaces, middleware, infrastructure code) is human-owned and rarely changes.

- ALWAYS extend or use skeleton base classes when building new features.
- NEVER modify skeleton files without explicit permission.
- NEVER reinvent patterns that the skeleton already provides (error handling, auth, validation, logging, API response formats).
- If you think a skeleton change is needed, propose it — do not implement it.
-->

### Pattern Consistency

As shared patterns emerge (error handling, auth, validation, logging, API response formats), treat them as established conventions. Do NOT reinvent them per feature. If you think an established pattern needs to change, propose it — do not implement the change unilaterally.

### Shared Code Rules

- Vue composables for shared logic go in the shared composables directory.
- Reusable Vue components go in the shared components directory.
- Backend shared utilities go in the shared directory.
- Do NOT extract shared code prematurely. Only extract when the same logic appears in 3+ features.
- Some duplication between slices is acceptable and preferred over wrong abstractions.

### Supabase as Source of Truth

- The Supabase schema defines all data types. Generated types from the schema are authoritative.
- Do NOT create ad-hoc type definitions in feature code that conflict with schema types.
- If a feature needs a type that doesn't exist in the schema, propose a migration first.


## Context Window Management

YOU MUST be aware of context limits. These rules help maintain output quality:

- Keep focus on the current task ONLY. Do not load unrelated files into context.
- When referencing existing code, read only the specific files needed — not the entire codebase.
- If a task requires understanding a pattern, read ONE good reference feature, not all features.
- If you notice yourself producing inconsistent or repetitive code, flag that context may be degrading.
- Do NOT maintain a growing TODO list in conversation. Keep task scope to what was explicitly asked.


## The Do's

- DO follow existing patterns. When a reference feature exists, match its structure exactly.
- DO write tests for every feature slice.
- DO use the project's established error handling, validation, and response patterns.
- DO keep files focused — one handler per file, one service per file, one composable per file.
- DO name files consistently using established naming conventions.
- DO suggest a commit message when a slice is complete and tested.
- DO ask before making architectural decisions that affect multiple features.
- DO provide clear explanations when something doesn't work as expected.
- DO check that new code is consistent with existing conventions before presenting it.
- DO use shadcn-vue components where appropriate rather than building custom UI from scratch.
- DO use Tailwind utility classes for styling. No custom CSS unless Tailwind cannot achieve the result.
- DO design mobile-first — start with small screen layouts, then add responsive breakpoints.
- DO ensure all UI is accessible — semantic HTML, ARIA attributes, keyboard navigable.


## The Don'ts

- DON'T design or change the architecture without explicit approval.
- DON'T build backend and frontend for a feature in the same pass. Separate slices.
- DON'T create mega-files that handle multiple responsibilities.
- DON'T skip validation or error handling "for now" — include it from the start.
- DON'T add dependencies or libraries without asking first.
- DON'T modify tests to make them pass — fix the implementation instead.
- DON'T claim something is working without verifying. If you can't run it, say so.
- DON'T over-engineer. Build exactly what was asked for. No speculative abstractions, no unnecessary flexibility, no extra features.
- DON'T create files outside the established folder structure without asking.
- DON'T put TODO comments in code as a substitute for actual implementation.
- DON'T forget cross-cutting concerns — every feature must use the project's established auth, error handling, and logging patterns.
- DON'T define types that conflict with the Supabase schema.
- DON'T use `any` in TypeScript without explicit justification.


## When Starting a New Feature

Follow this exact checklist:

1. Read the task requirements carefully.
2. Read the spec (if relevant to this feature).
3. Read ONE existing reference feature to understand the established pattern.
4. Read any shared patterns or base utilities this feature will use.
5. Present a brief plan: files to create, data flow, test approach.
6. Wait for approval.
7. Implement the backend slice first. Write tests, then implementation.
8. Confirm backend tests pass. Suggest a commit.
9. Implement the frontend slice. Write tests, then implementation.
10. Confirm frontend tests pass. Suggest a commit.


## When Something Goes Wrong

- If a test fails, read the error carefully and fix the root cause. Do not patch symptoms.
- If you're going in circles on a bug (3+ failed attempts), stop and present what you've tried and what you think the root cause might be. Ask for guidance.
- If you realize the current approach has a fundamental flaw, say so immediately rather than continuing to build on a broken foundation.
- If context feels degraded (you're forgetting earlier decisions or producing inconsistent code), flag it and suggest starting a fresh session.
