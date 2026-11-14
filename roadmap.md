# Home Central — Roadmap

Each milestone starts with a planning session that produces `specs/milestone-N.md`. Implementation starts only after that spec is approved.

| # | Milestone | Status |
|---|---|---|
| 1 | Foundation reset | Done |
| 2 | Properties and projects | In progress |
| 3 | Property profile and assets | Not started |
| 4 | Items, inventory, and project materials | Not started |
| 5 | Shopping list | Not started |
| 6 | AI project assistant | Not started |
| 7 | Recurring maintenance | Not started |
| 8 | Availability and smart scheduler | Not started |
| 9 | Reminders and dashboard | Not started |
| 10 | Production and mobile | Not started |

## 1. Foundation reset

Move off Supabase to a local stack that can be tested for real.

- Python virtual environment and a documented setup for backend and frontend
- SQLite + SQLModel + Alembic, with an in-memory database for tests
- `get_current_user` returns a seeded dev user
- Generate frontend API types from the backend OpenAPI schema
- Remove the Supabase client, mocks, and migrations
- Agree on the data model (planning output of this milestone)

## 2. Properties and projects

The core record everything else attaches to. A property is any place a user maintains: their home, a rental, a parent's house, a church.

- Properties with members and roles (owner, editor, viewer); a user can have several
- Projects belong to a property: title, description, status, priority (low to urgent), due date, assignee
- Project steps as their own rows: ordered, each with an estimate, wait time after, and whether it must stay in the same session as the next step
- Port the existing project pages, fix the instruction/material shape mismatch, add a project detail page

Existing work: the auth and project CRUD code from the Supabase stack, and the uncommitted project pages. Reuse the frontend where it fits.

## 3. Property profile and assets

What makes advice tailored.

- Home details: year built, size, climate zone
- Assets: HVAC, water heater, appliances, with brand, model, install date, and specs such as filter size
- Projects can reference an asset

## 4. Items, inventory, and project materials

- A per-home item catalog: tools vs. consumables, unit, quantity on hand, typical cost
- Project materials link a project to items with the quantity needed
- Project cost estimate is derived from materials plus other costs

## 5. Shopping list

- Computed, not stored: materials needed by upcoming projects minus what's on hand, grouped by item
- Marking an item bought adds it to inventory
- Remaining cost per project and in total

## 6. AI project assistant

- Describe a project in text (voice later) and answer clarifying questions
- Generates steps, materials, time and cost estimates, and learning resources into a draft project for the user to review
- Conversation stored per project

## 7. Recurring maintenance

- Recurring tasks with an interval (every N days/weeks/months/years) or a seasonal window
- Each due occurrence becomes a maintenance project, so it is scheduled, costed, and shopped for like any other project
- Suggested tasks based on the home profile and assets

## 8. Availability and smart scheduler

- The user's weekly availability windows and exceptions
- The scheduler places projects or steps into windows by priority, due date, duration, and whether materials are on hand
- Users can pin blocks so they don't get rescheduled; calendar view

## 9. Reminders and dashboard

- Reminders for due maintenance and scheduled work (email first, web push later)
- A "what's next" dashboard: this week's work, overdue maintenance, items to buy

## 10. Production and mobile

- Choose and set up real auth and the production database
- Invite other users to a property by email
- Deploy
- Mobile: start as an installable PWA; wrap it with Capacitor or build native when App Store presence or native features are needed
