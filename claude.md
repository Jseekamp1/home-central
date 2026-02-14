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

## Development Guidelines

- Build features in vertical slices within frontend and backend independently
- Use Vue composables for shared logic across components
- Reusable Vue components live in a shared directory, not duplicated per feature
- TypeScript strict mode across the frontend
- Keep the Supabase schema as the single source of truth for data types — generate/share types from it
