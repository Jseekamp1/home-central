# Home Central — TODO

## Auth + Dashboard (Milestone 1)

### Backend
- [x] Set up FastAPI project structure with Supabase client
- [x] Configure Supabase Auth (email/password sign-up and login)
- [x] Create `/auth/signup` and `/auth/login` API endpoints
- [x] Create `/auth/me` endpoint to return the authenticated user
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
- [x] Write tests for auth composable logic
- [ ] Write tests for login/sign-up form validation
- [ ] Write tests for route guard behavior (redirect when unauthenticated)
