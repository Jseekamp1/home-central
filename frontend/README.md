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

## UI components

Styling is Tailwind CSS v4 (`app/assets/css/main.css`, which also holds the theme colors). UI primitives come from [shadcn-vue](https://www.shadcn-vue.com/) and live in `app/shared/components/ui/`, one folder per component. They are our code: edit them freely.

To add one, copy its source from the shadcn-vue site (new-york style) into a new folder there, with imports pointing at `~/shared/lib/utils`. The `shadcn-vue add` CLI currently tries to install an unrelated npm package named `cn` with this setup, so don't use it until that's sorted out.

## Type check

```bash
npm run typecheck
```

## Tests

```bash
npm test
```

Run one feature's tests with `npx vitest run app/features/<feature>`.
