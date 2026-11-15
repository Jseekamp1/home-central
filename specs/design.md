# Design Direction

**Status:** Approved

Mockups: the "Direction A · Week-first" page of the [Home Central Design Direction](https://claude.ai/artifact/XDv6kgE3Cvkg3zc7T1joPZ) canvas (private to the owner). The "First pass" page is kept for reference only.

## What the app is built around

Home Central is **time-first and voice-first**. Lists and settings support three moments:

1. **Talk out a project.** One button, a few seconds, and you're describing a project. The assistant asks short follow-ups and fills in a draft you confirm.
2. **See your week.** The home screen is your free time with projects placed into it, not a to-do list.
3. **Change your time.** Say "I'm free Saturday afternoon" or "Sunday's gone", or edit your Google Calendar. The week is re-planned and the changes are shown.

## Navigation

- **Phone:** a bottom bar with Week, Projects, **Talk** (a large round button in the middle), Shop and More.
- **Desktop:** the same items in a left sidebar, with the property switcher at its top and Talk as a prominent button.
- **More** holds everything without its own tab: property settings and "Add a property" today; Google Calendar, inventory and maintenance later.
- **Property switcher:** the property name at the top of the screen. Tapping it opens a sheet listing **All properties** first, then each property with its color dot and your role, plus "Add a property" and that property's settings.
- **All properties** mixes every property's items into one view: the Week strip stacks each day's segments in their property colors, window and item cards carry a color dot and the property name, and the Projects list shows the property on every card. Choosing one property filters back down, and project time is shown in green again.
- Items appear only when their milestone ships. Until the Week screen exists (Milestone 6), Projects is the home screen; until the assistant exists (Milestone 4), there is no Talk button.

## Visual system: graphite and green

One theme, between dark and light: a mid-graphite background, not black. Everything sits in **outlined panels**: a slightly lighter gray fill with a thin border, never a light filled card. No separate light or dark mode for now.

| Token | Value | Used for |
|---|---|---|
| Background | `#2B2F33`, with a soft lift to `#33383D` at the top | Screen background |
| Panel | `#363B40` with a 1 px `#474D54` border | Every card: planned projects, the draft project, sheets, settings groups, assistant messages |
| Border | `#474D54` | Panel edges, dividers inside panels |
| Text | `#E3E7EB` | Body text |
| Muted text | `#A9B1B9` | Secondary text, labels |
| Your words | Fill `rgba(60,203,127,0.10)`, 1 px border `rgba(95,200,145,0.55)` | Things you said or typed to the assistant, so they read apart from its replies |
| Green | `#3CCB7F`, text on it `#1C2024` | Talk button, primary actions, selected chips, synced state, focus |
| Free-time line | `#5FC891` dashed; label `#7DD6A8` | Free time outlines and their labels |
| Attention | `#F2B860` | Unconfirmed guesses, as a dashed `#F2B860` outline with `#F2B860` text |
| Danger | `#F28B82` on background; urgent badge `#F8D3D0` / `#8F1D16` | Removed time, destructive actions, urgent |

### Property colors

Each person picks a color for each property they can see; it's personal, not shared. A new property gets the first color that person isn't using yet.

| Key | Value | Contrast on background / panel |
|---|---|---|
| `sky` | `#6CB4EE` | 6.0 / 5.1 |
| `teal` | `#4FD1C5` | 7.2 / 6.1 |
| `lime` | `#A3D977` | 8.2 / 6.9 |
| `violet` | `#A78BFA` | 5.0 / 4.2 |
| `pink` | `#F28CB8` | 5.9 / 5.0 |
| `coral` | `#F4977A` | 6.1 / 5.1 |
| `sand` | `#D9C3A0` | 7.9 / 6.6 |
| `slate` | `#9AA9BA` | 5.6 / 4.7 |

Property colors are used as dots, small bars and segments, never as text or fill behind text. Color is never the only cue: wherever it marks a property, the property's name is shown or announced too.

**Type:** Geist for titles, Inter for body text, Geist Mono for times, durations and small labels.

**Shape:** 12 px corners on panels and free-time outlines, 8 px on panels nested inside them. Controls are at least 44 px on touch screens and may be more compact (never under 24 px) with a mouse; small chips keep their look and get an enlarged touch area instead.

All text meets WCAG AA contrast (4.5:1) against the surface it sits on. Any new color pair must be checked before use.

## The Week screen

One connected view, top to bottom:

Project time is **always filled**: the scheduler chooses what goes into each window from the backlog. There is no "waiting" list on this screen; anything not scheduled is simply in the backlog (Projects).

1. **Title:** "This week" and the dates. No totals.
2. **Week strip:** one panel with seven day columns. Each shows its date and a bar whose height is that day's project time, split into one segment per scheduled item (done items turn gray). Days without project time show a flat line. Tapping a day selects it.
3. **Day / Week switch:** Day shows the selected day; Week shows every window in the week in order.
4. **Project-time windows:** each window is its own panel. Its header is a source icon (calendar = from Google Calendar, microphone = added by voice; each with an accessible label), the time range, and an "Edit" button. Inside are its scheduled items. Each item card shows the title with its own time range on the right, and the steps below. No durations are repeated: the window shows its range once, each item shows its range once. In Week view, the day name sits above each day's windows.
5. **Item actions:** swipe an item, or tap it, to reveal **Done**, **Swap** (send it back to the backlog and let the scheduler pick another) and **Cancel** (cancel the project). Tapping also shows why the scheduler put it there. The freed time is refilled immediately, and a status line confirms what happened, with Undo.
6. A day with no project time says so and offers "Add project time".

## The pieces

- **Project time** is green: the week strip bars, and the time range on each window panel. In the Talk and calendar screens it is drawn as a dashed green outline.
- **Scheduled work** is an outlined panel inside its window, showing the project, which steps and the time.
- **Guesses vs. your numbers:** anything the assistant isn't sure of is drawn dashed in amber with a "?" until you confirm or change it. Your own numbers are bold.
- **Status and priority** are text labels; color supports them but never carries meaning alone.

## Interaction rules

- **The scheduler fills your time; you steer it.** Adding a project or changing project time re-plans automatically. You can mark items done, swap them, cancel them or pin them. The assistant never buys or deletes anything on its own.
- **Show what changed.** Re-planning lists time added, time removed, what moved and what went back to the backlog, with Undo.
- **Disabled buttons say why**, e.g. "2 steps need an estimate".
- **Only permanent actions get a confirmation dialog**, which states exactly what will be lost, with the safe choice first and named for what it does ("Keep it"). Reversible actions just happen and show a short status line.
- **Loading** shows placeholder shapes, not spinners. **Errors** say what happened and offer a retry.
- **Voice is never the only way.** Every Talk screen has "Type instead", and everything said is shown as text.

## Google Calendar

Free time comes from one of: a dedicated calendar (default, e.g. "Home projects"), a tag in event titles (e.g. `#home`), or one event color. Options: write scheduled work back to that calendar, and skip time that overlaps other events. Changes in the calendar re-plan the week.

## Building it

- Theme tokens live in `frontend/app/assets/css/main.css` as the shadcn-vue variables; components use the tokens, never raw hex values.
- Before the first frontend slice built in this design, install [Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance) as agent tooling (not an app dependency) and use it for HTML, CSS and accessibility decisions. Review what it adds to the project before committing, and keep it only if it proves useful.
