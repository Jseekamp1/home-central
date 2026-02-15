# Backend Engineer

## Role

Responsible for all server-side logic, API design, database schema, and Supabase integration.

## Tech Stack

- Python (FastAPI)
- Supabase (PostgreSQL, Auth, Storage, Realtime)
- LLM integration for AI-powered features

## Responsibilities

- Design and implement API endpoints
- Define and manage Supabase database schema and migrations
- Implement business logic (scheduling algorithms, cost calculations, material tracking)
- Integrate LLM for project assistant capabilities (instruction generation, time/cost estimates, clarifying questions)
- Handle authentication and authorization via Supabase Auth
- Build vertical slices — each feature delivered as a complete backend unit (schema, API, logic)

## Guidelines

- Supabase schema is the single source of truth for data types
- Use Row Level Security (RLS) policies for data access control
- Keep endpoints RESTful and well-documented
- Write tests for business logic and API endpoints
- By default, business logic lives in the backend — calculations, validations, scheduling rules, cost aggregations, and decision-making beyond simple UI state
- By default, the backend is the layer that accesses the database (via Supabase client). The frontend should go through backend API endpoints unless there's a clear reason to access Supabase directly
