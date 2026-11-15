# Home Central — Roadmap

Each milestone starts with a planning session that produces `specs/milestone-N.md`. Implementation starts only after that spec is approved. The design for all milestones is in `specs/design.md`; every user flow is listed in `specs/user-flows.md`.

The order delivers value from the first minute (setup questions), then the core loop: **talk out a project → find project time → schedule it**. Supporting features (materials, shopping, profile, seasonal maintenance) follow.

| # | Milestone | Status |
|---|---|---|
| 1 | Foundation reset | Done |
| 2 | Properties and projects | Done |
| 3 | Setup questions and recurring basics | Not started |
| 4 | Talk out a project | Not started |
| 5 | Project time and Google Calendar | Not started |
| 6 | Scheduler and the Week screen | Not started |
| 7 | Materials, tools and inventory | Not started |
| 8 | Shopping list | Not started |
| 9 | Property profile and seasonal maintenance | Not started |
| 10 | Reminders, production and mobile | Not started |

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
- Personal property colors and an "All properties" view (hidden with one property)
- Projects belong to a property: title, description, status, priority (low to urgent), due date, assignee
- Project steps as their own rows: ordered, each with an estimate, wait time after, and whether it must stay in the same session as the next step
- The app shell and theme from `specs/design.md`; Projects is the home screen until Milestone 6

## 3. Setup questions and recurring basics

Make a new property useful in the first minute.

- After creating a property, a short questionnaire:
  - **Recurring tasks:** a common list (furnace filter, smoke alarms, gutters…), all checked, with "Unselect all"; then "Anything else?" to add your own
  - **Projects to do:** jot a list of titles; each becomes a draft project
  - A summary of what was set up
- Skip a step or skip everything; skipping first says the questions can be run again from property settings
- Run the questions again from property settings, without duplicating what's already there
- Recurring tasks with simple timing: every N days/weeks/months/years after the last completion, or in set months. Due occurrences become maintenance projects
- Property systems learned from the answers (checking "Change furnace filter" records a furnace)

## 4. Talk out a project

The assistant that turns a quick description into a planned project.

- The Talk button: speak (recorded in the browser, transcribed on the server) or type
- A back-and-forth in text: short follow-up questions, one at a time
- A draft project fills in as you talk: title, steps, time estimates. Guesses are marked until you confirm them
- You confirm the draft to create the project; the conversation is stored with it
- Draft projects from the setup questions can be talked through to fill them in
- Uses Claude through the Anthropic SDK in the backend; transcription service chosen in this milestone's planning

## 5. Project time and Google Calendar

Where your available time comes from.

- Connect Google Calendar (read access to one calendar)
- Project time from a dedicated calendar, a title tag, or an event color; optionally skip overlaps with other events
- Add or remove project time by talking ("I'm free Saturday afternoon", "Sunday's gone")
- Calendar changes are picked up automatically

## 6. Scheduler and the Week screen

The payoff: your week, planned.

- Fills all project time with ready projects and due maintenance, or their steps, chosen by priority, due date, fit and step order (wait time, keep together)
- The Week screen becomes home: the week strip, Day / Week views, and each project-time window with its scheduled items
- Swipe or tap an item to mark it done, swap it for another from the backlog, or cancel it; the time is refilled immediately, with Undo
- Re-plans when project time or projects change, and shows what moved, with Undo
- Optionally writes scheduled work back to Google Calendar
- Users can pin blocks so they don't move

## 7. Materials, tools and inventory

- Tools belong to a user; consumables belong to a property
- Tools are learned as you plan projects: "This needs a drill and a level. Do you have them?"
- Project materials link a project to items with the quantity needed; finishing a project uses up consumables
- The assistant asks about materials and what you already have
- The scheduler can prefer projects whose materials are on hand

## 8. Shopping list

- Computed, not stored: materials and tools needed by upcoming projects minus what you have
- Marking an item bought adds it to inventory
- Remaining cost per project and in total

## 9. Property profile and seasonal maintenance

What makes advice tailored.

- Property details: year built, size, climate zone, frost dates (estimated by the assistant, confirmed by you)
- Property systems in detail: brand, model, install date, and specs such as filter size or grass type
- Seasonal recurring tasks, timed from frost dates (e.g. overseeding in spring and fall)
- Suggested tasks based on the property profile and its systems

## 10. Reminders, production and mobile

- Reminders for due maintenance and scheduled work
- Choose and set up real auth and the production database
- Invite other users to a property by email
- Deploy
- Mobile: start as an installable PWA; wrap it with Capacitor or build native when App Store presence or native features are needed
