# Milestone 1 — Foundation Reset

**Status:** Draft, awaiting approval

## Goal

Replace the Supabase stack with a local one that can be tested for real, and agree on the target data model before any more features are built.

## Decisions

| Topic | Decision |
|---|---|
| Database | SQLite locally via SQLModel, migrations with Alembic. Schema stays Postgres-compatible. Production database decided in Milestone 10. |
| Supabase | Removed entirely: client, settings, mocks, and both migration folders. |
| Auth | `get_current_user` returns a seeded dev user. The `/auth/*` endpoints, login/signup pages, and auth middleware are removed now and rebuilt in Milestone 10 with the real provider. |
| Frontend rendering | `ssr: false`. The app runs as a static SPA so it can later be wrapped for mobile. |
| API types | Frontend types generated from the backend OpenAPI schema with `openapi-typescript`. |
| Top-level container | A **property**, not a "home", so it also covers a church, a parent's house, or a rental. |
| Property access | A user can own several properties and be invited to others. Access is through membership with a role. |
| Priority | `low`, `medium`, `high`, `urgent`, plus an optional due date. |
| Consumables | Finishing a project subtracts the consumables it used from inventory. Tools are never subtracted. |
| Ownership of items | Tools belong to a user and go wherever that user works. Consumables belong to a property. |
| Viewers | Read-only. They cannot create, propose, or change anything. |
| Splitting projects | The scheduler may spread a project across sessions, at step boundaries, following the step rules below. |
| Recurrence | Three kinds: a set time after the last completion, fixed calendar dates, and seasonal windows that adjust to the property's climate. |

### New dependencies (approved with this spec)

- Backend: `sqlmodel`, `alembic`. Remove `supabase`.
- Frontend (dev): `openapi-typescript`.

## Target data model

Each table is created in the milestone that first uses it, so this milestone only builds `users`. The rest is the agreed target, so later milestones don't redesign it.

Conventions: UUID primary keys, `created_at` and `updated_at` on every table, money in integer cents, durations in integer minutes, enums stored as text with check constraints. JSON columns hold display-only data only. Anything queried across rows gets its own table.

### People and properties

| Table | Fields | Milestone |
|---|---|---|
| `users` | email, display_name | 1 |
| `properties` | name, kind (`home`, `rental`, `family`, `organization`, `other`), address_line, postal_code, climate_zone, last_spring_frost (month-day), first_fall_frost (month-day), year_built, square_feet, notes | 2 (details in 3) |
| `property_members` | property_id, user_id, role (`owner`, `editor`, `viewer`). Unique per property and user. | 2 |
| `property_assets` | property_id, kind (`hvac`, `water_heater`, `appliance`, `lawn`, …), name, brand, model, install_date, specs (JSON, e.g. filter size, grass type) | 3 |

The frost dates are estimated by the LLM from the postal code when the property is created (Milestone 3). The user sees and confirms them, and can change them at any time. A lawn is an asset, so its grass type can drive which seasonal tasks apply.

Access rule: every query for property data joins through `property_members` for the current user. Viewers can only read. Editors can create and change projects, items, and tasks. Only owners can delete the property or manage members. Every property has at least one owner.

### Projects

| Table | Fields | Milestone |
|---|---|---|
| `projects` | property_id, kind (`project`, `maintenance`), title, description, status (`draft`, `ready`, `in_progress`, `done`, `cancelled`), priority, due_date, other_cost_cents, asset_id?, recurring_task_id?, assignee_id? (a property member), source (`manual`, `ai`), resources (JSON), completed_at | 2 |
| `project_steps` | project_id, position, title, details, estimated_minutes, wait_after_minutes, keep_with_next, done_at | 2 |

Calculated, never stored: total duration (sum of steps), estimated cost (materials plus `other_cost_cents`), and whether a project is scheduled.

**Step rules for splitting projects:**
- `wait_after_minutes` is time that must pass before the next step, such as paint drying or caulk curing. The scheduler can fill that gap with other work.
- `keep_with_next` means the next step must happen in the same session, such as "turn off the water" followed by "replace the valve".
- A session never ends partway through a step.

### Items and materials

| Table | Fields | Milestone |
|---|---|---|
| `items` | kind (`tool`, `consumable`), user_id (tools only), property_id (consumables only), name, unit, quantity_on_hand, typical_unit_cost_cents | 4 |
| `project_materials` | project_id, item_id, quantity_needed, unit_cost_cents? (overrides the typical cost) | 4 |

A check constraint makes sure a tool has a `user_id` and no `property_id`, and a consumable the reverse.

When a project is marked done, the user confirms how much of each consumable was used. The default is `quantity_needed`, and inventory is reduced by that amount, never below zero.

The shopping list is calculated for open projects:
- Consumables: quantity needed minus what that property has on hand.
- Tools: needed if the person doing the work (the assignee, or the current user when unassigned) doesn't own one.

### Recurring maintenance

| Table | Fields | Milestone |
|---|---|---|
| `recurring_tasks` | property_id, asset_id?, title, description, rule_type (`after_completion`, `calendar`, `seasonal`), rule (JSON, shape depends on rule_type), lead_days, template_steps (JSON), template_materials (JSON), active | 7 |

Rule types:
- `after_completion`: due a set time after the last one was finished, e.g. 90 days after the last filter change. Rule: `{interval_count, interval_unit}`, where the unit is `day`, `week`, `month`, or `year`.
- `calendar`: due on fixed dates, e.g. clean gutters every April and October. Rule: `{months, day_of_month}`.
- `seasonal`: one or more windows defined relative to the property's frost dates, so the same task lands at different times in different places. Rule: a list of windows, each `{anchor, start_offset_days, end_offset_days}`, where the anchor is `last_spring_frost` or `first_fall_frost`.

Example: overseed a cool-season lawn in spring and fall.
```json
[
  {"anchor": "last_spring_frost", "start_offset_days": 14,  "end_offset_days": 45},
  {"anchor": "first_fall_frost",  "start_offset_days": -60, "end_offset_days": -30}
]
```
With frost dates of April 20 and October 15, that gives May 4 – June 4 and August 16 – September 15. A property further south gets earlier spring and later fall windows from the same task.

Occurrences:
- `lead_days` days before an occurrence is due, it is created as a `maintenance` project. Only one open occurrence exists per task at a time.
- For seasonal tasks, the project is due at the end of its window. The scheduler may only place it inside the window.
- A window that passes without completion is marked missed, and the next window's occurrence is created.

### Scheduling and assistant

| Table | Fields | Milestone |
|---|---|---|
| `availability_windows` | user_id, weekday, start_time, end_time | 8 |
| `schedule_blocks` | user_id, project_id, step_ids (the steps covered in this session), starts_at, ends_at, pinned | 8 |
| `assistant_messages` | project_id, role (`user`, `assistant`), content | 6 |

Availability and schedules belong to a user, not a property, because one person's time covers all their properties.

## Milestone 1 scope

1. Backend Python virtual environment and a setup section in a README.
2. Swap the Supabase dependency for SQLModel and Alembic. Settings use a `DATABASE_URL` that defaults to a local SQLite file.
3. `users` table with the first Alembic migration, plus a seed for the dev user.
4. `get_current_user` returns the dev user from the database.
5. Test fixtures: in-memory SQLite per test, a FastAPI test client, no Supabase mocks.
6. Delete: `app/supabase_client.py`, the auth router and its tests, `backend/migrations/`, `supabase/`, the old Supabase-mocking project tests, the login/signup pages, and the auth middleware and composable.
7. Frontend: set `ssr: false`, add a script that generates API types from `/openapi.json`, and add an API wrapper with no token handling.
8. Keep the uncommitted project pages and components out of this milestone. They are ported in Milestone 2.

The existing backend `projects` feature is removed here and rebuilt on the new model in Milestone 2.

## Tests worth keeping

- `GET /me` returns the dev user, proving the database, seed, and auth dependency are wired together.
- A migration test: running Alembic on an empty database gives the same schema as the models.

## Done when

- `pytest` passes with no network access and no Supabase installed.
- `npm run dev` loads the app with no login screen.
- Generated frontend types match the backend schema.
- No references to Supabase remain in the code.

## Open questions

None.
