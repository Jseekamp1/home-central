# Milestone 2 — Properties and Projects

**Status:** Approved

## Goal

A user can set up one or more properties, switch between them, and plan projects at each one as an ordered list of steps they check off as they go.

## Decisions

Decided by you in planning:

| Topic | Decision |
|---|---|
| First run | A user with no property sees a short setup form (name, kind, postal code) before anything else. |
| Projects list | A property switcher in the header picks the current property; the projects list shows that property's projects. |
| Status | Mostly automatic. Checking off a step on a `draft` or `ready` project moves it to `in_progress`. Checking off the last open step offers to mark it `done`. The user can always set the status by hand. |
| Removing a project | **Cancel** keeps it in history, out of the active list. **Delete** removes it permanently after confirmation. |
| Time estimates | Required to schedule, optional while planning. A project can only be marked `ready` when it has at least one step and every step has an estimate. Drafts can have gaps. |
| UI components | Upgrade to Tailwind v4 and adopt shadcn-vue for UI primitives (select, dialog, inputs, buttons). |

Recommended defaults (change any of these before approving):

| Topic | Default |
|---|---|
| Remembering the current property | Stored per device in the browser. If it's missing or no longer accessible, use the first property. |
| Who can edit property details | Owners and editors. Only owners can delete a property. |
| Deleting a property | Owner only, after a confirmation that says how many projects will be deleted with it. |
| Moving a project to another property | Not in this milestone. |
| `draft` vs `ready` | `draft` = still being planned. `ready` = fully estimated and ready to be scheduled. Always set by hand. |
| Leaving `done` | Setting `done` records `completed_at`; moving out of `done` clears it. |
| Estimates after `ready` | The estimate rule only gates the move into `ready`. If a step without an estimate is added later, the project keeps its status and the step is flagged "needs estimate". The Milestone 8 scheduler skips flagged steps and lists them for the user. |
| Entering estimates | The step form puts the estimate next to the title, with quick picks (15 min, 30 min, 1 h, 2 h, 4 h) plus a custom value. The project shows the total and "N steps need an estimate". |
| Reordering steps | Move up / move down buttons: accessible and touch-friendly. Drag-and-drop can come later. |
| Step scheduling fields | `wait_after_minutes` and `keep_with_next` are stored now but get no UI until Milestone 8. |
| Assignee | Column added now, empty, with no UI until other users exist (Milestone 10). |
| Columns for later milestones | `other_cost_cents`, `resources`, `asset_id`, `recurring_task_id`, `source`, and `kind` are added in the milestones that use them, not now. |

## Data

Created in this milestone (from the target model in `milestone-1.md`):

**`properties`**: name (1–100 chars), kind (`home`, `rental`, `family`, `organization`, `other`), postal_code (1–20 chars, required), address_line (optional), notes (optional). Profile fields (climate, frost dates, year built, size) come in Milestone 3.

**`property_members`**: property_id, user_id, role (`owner`, `editor`, `viewer`). Unique per property and user. Creating a property makes the creator its owner.

**`projects`**: property_id, title (1–200 chars), description (up to 5,000 chars), status, priority (`low`, `medium`, `high`, `urgent`; default `medium`), due_date (optional; a past date is allowed and shown as overdue), assignee_id (optional), completed_at.

**`project_steps`**: project_id, position, title (1–200 chars), details (optional), estimated_minutes (optional, ≥ 0), wait_after_minutes (default 0), keep_with_next (default false), done_at.

Deleting a property deletes its members, projects, and steps. Deleting a project deletes its steps.

## Permissions

| Action | Viewer | Editor | Owner |
|---|---|---|---|
| See the property, its projects and steps | ✓ | ✓ | ✓ |
| Create, change, or delete projects and steps | | ✓ | ✓ |
| Edit property details | | ✓ | ✓ |
| Delete the property | | | ✓ |

- A user who isn't a member gets **404**, so the API doesn't reveal that the property exists.
- A member without permission gets **403**.
- Responses include the caller's role, so the UI can hide controls a viewer can't use.
- Inviting members needs real accounts (Milestone 10). Until then, tests create the second user directly in the database.

## API

| Method | Path | Notes |
|---|---|---|
| GET | `/properties` | The caller's properties, with their role in each |
| POST | `/properties` | Creator becomes owner |
| GET | `/properties/{id}` | |
| PATCH | `/properties/{id}` | Owner or editor |
| DELETE | `/properties/{id}` | Owner; deletes everything in it |
| GET | `/properties/{id}/projects?view=active\|done\|cancelled` | `active` = draft, ready, in progress (default) |
| POST | `/properties/{id}/projects` | |
| GET | `/projects/{id}` | Includes steps, the estimate total, and the count of unestimated steps |
| PATCH | `/projects/{id}` | Fields and status |
| DELETE | `/projects/{id}` | Permanent |
| POST | `/projects/{id}/steps` | Added at the end |
| PATCH | `/projects/{id}/steps/{step_id}` | Fields, and done/undone |
| DELETE | `/projects/{id}/steps/{step_id}` | Remaining steps are renumbered |
| PUT | `/projects/{id}/steps/order` | Body: every step id in the new order |

**Project list order:** priority (urgent first), then due date (soonest first, none last), then newest. Done projects are sorted by `completed_at`, newest first.

**Step rules:**
- Positions are always 1..N with no gaps.
- The reorder request must list exactly the project's current steps, or it's rejected with 422.
- Checking off a step on a `draft` or `ready` project sets the project to `in_progress`. This happens in the same request, and the response says so.
- Un-checking steps never changes the status.
- Setting a project to `ready` is rejected with 422 unless it has at least one step and every step has an estimate. The error names how many steps are missing one.

## Screens

Mobile-first.

- **Header:** the property switcher (a select, with "Add property…" at the end), plus links to Projects and Dashboard.
- **Setup** (`/setup`): name, kind, postal code. Shown automatically when the user has no property; also reachable from "Add property…".
- **Property settings** (`/property`): edit details. The owner can delete the property after a confirmation dialog.
- **Projects** (`/projects`): tabs for Active, Done, Cancelled. Cards show title, status, priority, due date (with an overdue marker), step progress ("3 of 7"), total estimate, and a "needs estimates" marker when any step lacks one.
- **New project** (`/projects/new`) and **Edit project** (`/projects/[id]/edit`): title, description, priority, due date, status.
- **Project detail** (`/projects/[id]`):
  - Step list: check off, add, edit, move up or down, delete.
  - Estimate total.
  - Status control. "Mark ready" is disabled with the reason shown (e.g. "2 steps need an estimate") until the project qualifies.
  - Steps without an estimate are visibly flagged.
  - Cancel and Delete actions.
  - When the last step is checked off: "All steps done. Mark project done?"
- **Viewers** see the same screens without any editing controls.

From the old pages on `wip/m2-old-project-pages`, reuse the layout and styling of `ProjectCard` and `ProjectForm`. The composable is rewritten on generated types.

## Slices

Each slice is a commit.

1. UI foundation: frontend only. Upgrade to Tailwind v4, set up shadcn-vue, restyle the existing layout and dashboard with it. No feature changes.
2. Properties: backend
3. Design direction: no code. Decide navigation, property switcher placement, visual style, and shared UI patterns for the whole app, with mockups of the app shell and key screens. Output: `specs/design.md`, approved before slice 4.
4. Properties: frontend (setup, switcher, settings)
5. Projects: backend
6. Projects: frontend (list, create, edit, detail without steps)
7. Steps: backend (including the `ready` rule)
8. Steps: frontend

## Tests worth keeping

- **Permissions:** for each role and for a non-member, which property and project actions are allowed (one table-driven test).
- **Status:** checking off a step moves a `ready` project to `in_progress`; un-checking leaves it alone; `ready` is refused while any step lacks an estimate or there are no steps.
- **Reorder:** a valid reorder gives positions 1..N in the new order, and a request with a missing or foreign step id is rejected.
- **Cascade:** deleting a property removes its projects and steps.

## Dependency changes (approved with this spec)

- Replace `@nuxtjs/tailwindcss` (Tailwind v3) with Tailwind v4 through `@tailwindcss/vite`.
- Add shadcn-vue and what it needs: `reka-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-vue-next` (icons), `tw-animate-css`. Its components are copied into the repo under `app/shared/components/ui/`.
- Dev: `vue-tsc`, so `.vue` files are type-checked (`npm run typecheck`).

## Done when

- A fresh database leads to the setup form, then to an empty projects list.
- Two properties can be created and switched between, each with its own projects.
- A project can be planned with steps, worked through, and finished, with status following the rules above.
- All tests pass and `npm run typecheck` is clean.
