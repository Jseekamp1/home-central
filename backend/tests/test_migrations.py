from pathlib import Path

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine
from sqlmodel import SQLModel

import app.models  # noqa: F401  (registers every table on SQLModel.metadata)

BACKEND_DIR = Path(__file__).resolve().parent.parent


def test_migrations_produce_the_same_schema_as_the_models(tmp_path):
    db_url = f"sqlite:///{tmp_path / 'migrations.db'}"
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    config.set_main_option("sqlalchemy.url", db_url)

    command.upgrade(config, "head")

    engine = create_engine(db_url)
    with engine.connect() as connection:
        diff = compare_metadata(MigrationContext.configure(connection), SQLModel.metadata)
    engine.dispose()

    assert diff == [], f"Models and migrations differ: {diff}"
