import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel

import app.models  # noqa: F401  (registers every table on SQLModel.metadata)
from app.features.users.models import User
from app.main import app as fastapi_app
from app.shared.db import get_session, make_engine
from app.shared.dependencies import get_current_user


@pytest.fixture
def engine():
    # One in-memory database per test; StaticPool keeps it on a single connection.
    engine = make_engine("sqlite://", poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(engine):
    def override_get_session():
        with Session(engine) as session:
            yield session

    fastapi_app.dependency_overrides[get_session] = override_get_session
    yield TestClient(fastapi_app)
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def make_user(session):
    """Create another user directly in the database (no sign-up flow yet)."""
    def _make_user(email: str) -> User:
        user = User(email=email, display_name=email.split("@")[0])
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    return _make_user


@pytest.fixture
def act_as(client):
    """Make subsequent requests come from the given user instead of the dev user."""
    def _act_as(user: User) -> None:
        fastapi_app.dependency_overrides[get_current_user] = lambda: user

    return _act_as
