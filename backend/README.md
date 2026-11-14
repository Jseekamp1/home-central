# Home Central — Backend

FastAPI + SQLModel, with SQLite for local development and Alembic for migrations.

## Setup

From `backend/`:

```bash
py -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"
.venv/Scripts/alembic upgrade head
```

Settings are optional; defaults are in `.env.example`. Copy it to `.env` to override.

## Run

```bash
.venv/Scripts/python -m uvicorn app.main:app --reload
```

The API runs at http://localhost:8000. Interactive docs are at `/docs`, and the schema the frontend generates types from is at `/openapi.json`.

Until real auth exists, every request acts as the dev user, created on first use.

## Tests

```bash
.venv/Scripts/python -m pytest
```

Tests use a fresh in-memory SQLite database each, through the real API. Run one feature's tests with `pytest app/features/<feature>`.

## Migrations

After changing a table model (and adding it to `app/models.py` if it's new):

```bash
.venv/Scripts/alembic revision --autogenerate -m "describe the change"
.venv/Scripts/alembic upgrade head
```

Review the generated file before committing. `tests/test_migrations.py` fails if models and migrations ever disagree.
