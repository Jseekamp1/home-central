from sqlmodel import select

from app.config import settings
from app.features.users.models import User


def test_me_returns_the_dev_user(client):
    response = client.get("/me")

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == settings.dev_user_email
    assert body["display_name"] == settings.dev_user_display_name
    assert body["id"]


def test_dev_user_is_created_once_and_reused(client, session):
    first = client.get("/me").json()
    second = client.get("/me").json()

    assert first["id"] == second["id"]
    users = session.exec(select(User)).all()
    assert len(users) == 1
