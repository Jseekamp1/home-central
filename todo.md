# Home Central — TODO

## Auth + Dashboard (Milestone 1)

### Backend
- [x] Set up FastAPI project structure with Supabase client
- [x] Configure Supabase Auth (email/password sign-up and login)
- [x] Create `/auth/signup` and `/auth/login` API endpoints
- [x] Create `/auth/me` endpoint to return the authenticated user
- [x] Restructure auth into feature-based folders (vertical slice architecture)
- [x] Extract `get_current_user` shared dependency
- [ ] Add auth middleware to protect routes
- [ ] Create `/dashboard` endpoint returning placeholder dashboard data
- [x] Write tests for all auth endpoints
- [ ] Write tests for protected route access (authorized vs unauthorized)

### Frontend
- [x] Set up Nuxt 3 project with TypeScript, Tailwind CSS, and shadcn-vue
- [x] Create login page with email/password form
- [x] Create sign-up page with email/password form
- [x] Add auth composable to manage login state and token storage
- [x] Add route middleware to redirect unauthenticated users to login
- [x] Create dashboard page — display authenticated user info as validation
- [x] Restructure auth into feature-based folders (composables + tests)
- [x] Write tests for auth composable logic
- [ ] Write tests for login/sign-up form validation
- [ ] Write tests for route guard behavior (redirect when unauthenticated)

---

## Project CRUD (Milestone 2)

### Planning
- [ ] Design projects table schema and RLS policies
- [ ] Define API contract (endpoints, request/response shapes, error cases)
- [ ] Identify frontend pages, components, and composables needed

### Backend
- [ ] Write Supabase migration SQL for projects table
- [ ] Write tests for project CRUD endpoints (create, list, get, update, delete, auth, 404)
- [ ] Create Pydantic models (ProjectCreate, ProjectUpdate, ProjectResponse)
- [ ] Implement projects router with CRUD endpoints
- [ ] Register projects router in main.py
- [ ] Verify all backend tests pass

### Frontend
- [ ] Create useApi composable (shared authenticated fetch wrapper)
- [ ] Write tests for useProjects composable
- [ ] Implement useProjects composable
- [ ] Build ProjectForm component
- [ ] Build ProjectCard component
- [ ] Build project list, create, and detail/edit pages
- [ ] Add projects link to navigation
- [ ] Verify all frontend tests pass

---

## Materials & Shopping Lists (Milestone 3)

### Planning
- [ ] Design materials table schema and RLS policies
- [ ] Define API contract for materials CRUD and shopping list endpoint
- [ ] Identify frontend pages, components, and composables needed

### Backend
- [ ] Write Supabase migration SQL for materials table
- [ ] Write tests for materials CRUD and shopping list endpoints
- [ ] Create Pydantic models for materials
- [ ] Implement materials router (nested under /projects/{id}/materials)
- [ ] Implement shopping list endpoint (GET /shopping-list)
- [ ] Register materials router in main.py
- [ ] Verify all backend tests pass

### Frontend
- [ ] Write tests for useMaterials and useShoppingList composables
- [ ] Implement useMaterials and useShoppingList composables
- [ ] Build MaterialItem component (with owned toggle)
- [ ] Build MaterialForm component
- [ ] Integrate materials into project detail page
- [ ] Build shopping list page
- [ ] Add shopping list to navigation
- [ ] Verify all frontend tests pass
