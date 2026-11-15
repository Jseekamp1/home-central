# User Flows

Every path a person can take through Home Central. Update this table whenever a flow is added, changed or built.

**Status:** Built = in the app · Designed = decided in a spec or mockup, not built · Planned = on the roadmap, details decided in that milestone's planning.

**Who:** Any = anyone signed in · Member = any role on the property · Editor = editor or owner · Owner = owner only.

## First run and properties

| # | Flow | Who | Starts from | Path | Ends at | Milestone | Status |
|---|---|---|---|---|---|---|---|
| P1 | First property | Any, no properties | Opening the app | Sent to setup → enter name, kind, postal code → Create | Home for the new property; from Milestone 3, the setup questions (S1) | 2 | Built |
| P2 | Fix a setup mistake | Any | Setup form | Submit with a missing field → focus jumps to it, error shown and announced → fix → Create | Home | 2 | Built |
| P3 | Add another property | Any | Switcher → "Add a property" | Setup form → Create (gets your next unused color) | Home for the new property | 2 | Built |
| P4 | Switch property | Any, 2+ properties | Property name at the top | Sheet → pick a property | That property, remembered on this device | 2 | Built |
| P5 | See all properties | Any, 2+ properties | Switcher → "All properties" | Pick it | Everything from every property, color-coded; remembered on this device | 2 (Week view: 6) | Built for home; projects and Week to come |
| P6 | One property only | Any, 1 property | Anywhere | No "All properties", no color dots, no color picker | — | 2 | Built |
| P7 | Pick your color for a property | Member, 2+ properties | Settings → "Your color" | Tap a swatch → saved instantly | Your own color; others keep theirs | 2 | Built |
| P8 | Edit property details | Editor | Settings | Change fields → Save → "Saved." | Settings | 2 | Built |
| P9 | View a shared property | Viewer | Settings | Read-only details with a note explaining why | Settings | 2 | Built |
| P10 | Delete a property | Owner | Settings → Delete | Confirmation focuses "Keep it" → Delete | Another property, or setup if none are left | 2 | Built |
| P11 | Back out of deleting | Owner | Delete confirmation | "Keep it", Esc, or tap outside | Settings, nothing deleted | 2 | Built |
| P12 | Server unreachable | Any | Any screen | Error banner → Try again | Where they were | 2 | Built |
| P13 | Invite someone to a property | Owner | Settings → Members | Enter email → choose role → Send | Invite pending until accepted | 10 | Planned |
| P14 | Accept an invite | Invitee | Email link | Sign in or sign up → accept | The shared property, with their own color | 10 | Planned |
| P15 | Fill in the property profile | Editor | Settings → Profile | Year built, size; frost dates estimated by the assistant → confirm or edit | Settings | 9 | Planned |
| P16 | Add an asset | Editor | Settings → Assets | HVAC, water heater, lawn… with model, install date, specs | Asset list | 9 | Planned |

## Setup questions

Shown after creating a property, so the app is useful from the first minute. Every step can be skipped, and the whole thing can be run again from settings.

| # | Flow | Who | Starts from | Path | Ends at | Milestone | Status |
|---|---|---|---|---|---|---|---|
| S1 | Answer the setup questions | Editor | Creating a property (P1, P3) | **Recurring tasks:** a common list (e.g. change furnace filter, test smoke alarms, clean gutters), all checked, each showing how often → uncheck any, or "Unselect all" → **Anything else?** add your own with how often → **Projects to do:** jot a list of titles → **Summary** of what was set up | Home, with recurring tasks and draft projects | 3 | Designed |
| S2 | Skip one step | Editor | Any setup step | "Skip this step" | The next step | 3 | Designed |
| S3 | Skip all of it | Editor | Any setup step | "Skip setup" → notice: you can run these questions again any time from property settings → Skip anyway, or Go back | Home | 3 | Designed |
| S4 | Run the setup questions again | Editor | Settings → "Setup questions" | Same steps; recurring tasks you already have show as checked, and nothing is duplicated | Settings | 3 | Designed |
| S5 | Property systems learned from answers | — | S1 or S4 | Checking a task that implies a system records it on the property, e.g. "Change furnace filter" records a furnace | Property's systems list | 3 | Designed |

## Projects and steps

| # | Flow | Who | Starts from | Path | Ends at | Milestone | Status |
|---|---|---|---|---|---|---|---|
| J1 | Create a project by hand | Editor | Projects → New | Title, description, priority, due date → Save | Project detail, status Draft | 2 | Designed |
| J2 | Browse projects | Member | Projects | Active / Done / Cancelled tabs; in All properties each card shows its property | Projects | 2 | Designed |
| J3 | Plan steps | Editor | Project detail | Add a step with title and a quick-pick estimate (15 min – 4 h, or custom) | Step list | 2 | Designed |
| J4 | Reorder steps | Editor | Project detail → Reorder | Move up / move down | Step list | 2 | Designed |
| J5 | Mark a project ready | Editor | Project detail | "Mark ready" is enabled once every step has an estimate; otherwise it says how many are missing | Ready to schedule | 2 | Designed |
| J6 | Work through steps | Editor | Project detail or Week | Check off a step → Draft or Ready moves to In progress | Project detail | 2 | Designed |
| J7 | Finish a project | Editor | Checking off the last step | "All steps done. Mark project done?" → Mark done | Done tab | 2 | Designed |
| J8 | Edit a project | Editor | Project detail → Edit | Change fields → Save | Project detail | 2 | Designed |
| J9 | Cancel a project | Editor | Project detail or Week item | Cancel → status line with Undo | Cancelled tab; its scheduled time is refilled | 2 (Week: 6) | Designed |
| J10 | Delete a project | Editor | Project detail → Delete | Confirmation focuses "Keep it" → Delete | Projects | 2 | Designed |
| J11 | Follow a project as a viewer | Viewer | Projects | Same screens, no editing controls | — | 2 | Designed |

## Talk out a project

| # | Flow | Who | Starts from | Path | Ends at | Milestone | Status |
|---|---|---|---|---|---|---|---|
| T1 | Describe a project by voice | Editor | Talk button | Speak → transcript shown → assistant asks one question at a time → draft card fills in (steps, estimates) → answer or correct guesses | Draft ready to confirm | 4 | Designed |
| T2 | Describe a project by typing | Editor | Talk → "Type instead" | Same as T1, typed | Draft ready to confirm | 4 | Designed |
| T3 | Confirm a draft | Editor | End of a conversation | "Add and schedule" | New project; scheduled automatically from Milestone 6 | 4 (scheduling: 6) | Designed |
| T4 | Keep a draft for later | Editor | End of a conversation | "Keep as draft" | Draft project in Projects | 4 | Designed |
| T5 | Correct a guess | Editor | Draft card | Tap a dashed amber estimate, or say the right number | Confirmed value shown in bold | 4 | Designed |
| T6 | Talk about materials | Editor | During a conversation | Assistant lists materials → tap the ones you have | Missing ones go to the shopping list | 7 | Designed |
| T7 | Microphone unavailable or denied | Editor | Talk button | Explains why → offers typing | T2 | 4 | Planned |

## Project time and Google Calendar

| # | Flow | Who | Starts from | Path | Ends at | Milestone | Status |
|---|---|---|---|---|---|---|---|
| C1 | Connect Google Calendar | Any | More → Google Calendar | Sign in with Google → choose where project time comes from (a calendar, a #tag, or a color) → options (write back, skip overlaps) | Week, filled from the calendar | 5 | Designed |
| C2 | Add project time by voice | Any | Talk | "I'm free Saturday afternoon" → summary of what changed → Looks good / Undo | Week, re-planned | 5 | Designed |
| C3 | Remove project time by voice | Any | Talk | "Sunday's gone" → what moved and what went back to the backlog → Looks good / Undo | Week, re-planned | 5 | Designed |
| C4 | Edit a time window | Any | Week → window → Edit | Change or remove the time | Week, re-planned | 5 | Designed |
| C5 | Calendar changes outside the app | Any | Google Calendar | The app picks up the change → re-plans | Week, with what changed | 5 | Designed |
| C6 | Disconnect Google Calendar | Any | More → Google Calendar | Disconnect → confirm | Project time only from voice and manual entries | 5 | Planned |

## Week and the scheduler

| # | Flow | Who | Starts from | Path | Ends at | Milestone | Status |
|---|---|---|---|---|---|---|---|
| W1 | Check this week | Any | Opening the app | Week strip → tap a day → its windows and items | Week | 6 | Designed |
| W2 | See the whole week | Any | Week → Week view | Every window in order | Week | 6 | Designed |
| W3 | Mark an item done | Editor | Week item (swipe or tap) | Done → status line with Undo | Item done; segment turns gray | 6 | Designed |
| W4 | Swap an item | Editor | Week item (swipe or tap) | Swap → back to the backlog; the scheduler picks another → Undo | Week | 6 | Designed |
| W5 | Cancel from the week | Editor | Week item (swipe or tap) | Cancel → time refilled → Undo | Week | 6 | Designed |
| W6 | Ask why something is scheduled | Any | Week item (tap) | Reason shown ("Urgent and overdue since Nov 10") | Week | 6 | Designed |
| W7 | Pin an item | Editor | Week item | Pin → it won't be moved when re-planning | Week | 6 | Planned |
| W8 | See everything across properties | Any, 2+ properties | Switcher → All properties | Each day's items from every property, in property colors | Week | 6 | Designed |
| W9 | No project time this day | Any | Week → a day without time | "No project time this day" → Add time | C2 / C4 | 6 | Designed |

## Materials, shopping and maintenance

| # | Flow | Who | Starts from | Path | Ends at | Milestone | Status |
|---|---|---|---|---|---|---|---|
| M1 | Add materials to a project | Editor | Project detail → Materials | Add items with quantities (tools are yours; consumables belong to the property) | Project materials | 7 | Planned |
| M2 | Record what you own | Any | More → Inventory | Add or adjust tools and consumables | Inventory | 7 | Planned |
| M8 | Tools learned from projects | Editor | Planning a project (by talking or by hand) | "This needs a drill, a stud finder and a level. Do you have them?" → tap the ones you own | Recorded as your tools; missing ones go to the shopping list | 7 | Designed |
| M3 | Use up consumables | Editor | Finishing a project | Confirm how much of each consumable was used | Inventory reduced | 7 | Planned |
| M4 | Shop for upcoming work | Any | Shop | Combined list across upcoming projects → check off bought items | Bought items added to inventory | 8 | Planned |
| M5 | Set up recurring maintenance | Editor | More → Maintenance, or the setup questions (S1) | Pick a common task or add your own → how often: every N days/weeks/months/years, or set months; seasonal timing from Milestone 9 | Recurring task | 3 | Planned |
| M6 | Maintenance comes due | — | Automatic | Due occurrence becomes a maintenance project → scheduled like any other once the scheduler exists (6) | Projects, then Week | 3 | Planned |
| M7 | Get a reminder | Any | Notification | Open it → the item in the Week | Week | 10 | Planned |
