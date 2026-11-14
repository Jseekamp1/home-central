from collections.abc import Iterator
from typing import Any

from sqlalchemy import Engine, event
from sqlmodel import Session, create_engine

from app.config import settings


def make_engine(url: str, **kwargs: Any) -> Engine:
    """Create an engine; on SQLite, turn on foreign keys (off by default)."""
    is_sqlite = url.startswith("sqlite")
    if is_sqlite:
        kwargs.setdefault("connect_args", {"check_same_thread": False})

    engine = create_engine(url, **kwargs)

    if is_sqlite:
        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(dbapi_connection, _record):
            dbapi_connection.execute("PRAGMA foreign_keys=ON")

    return engine


engine = make_engine(settings.database_url)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
