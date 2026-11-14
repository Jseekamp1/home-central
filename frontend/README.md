# Home Central — Frontend

Nuxt 4 single-page app (no server-side rendering) that talks to the backend API.

## Setup

```bash
npm install
```

## Run

Start the backend first (see `backend/README.md`), then:

```bash
npm run dev
```

The app runs at http://localhost:3000 and calls the API at `http://localhost:8000` (`runtimeConfig.public.apiBase` in `nuxt.config.ts`).

## API types

API types are generated from the backend, never hand-written. With the backend running:

```bash
npm run gen:api
```

This writes `app/shared/api/schema.d.ts`. Use the types through `Schemas` from `app/shared/api/types.ts`, e.g. `Schemas['UserRead']`. Re-run it after any backend model change and commit the result.

## Tests

```bash
npm test
```

Run one feature's tests with `npx vitest run app/features/<feature>`.
