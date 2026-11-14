from fastapi import Depends
from sqlmodel import Session, select

from app.config import settings
from app.features.users.models import User
from app.shared.db import get_session


def get_current_user(session: Session = Depends(get_session)) -> User:
    """Return the signed-in user.

    Until real auth exists (Milestone 10) this is always the dev user, created
    on first use so a fresh database needs no separate seed step. Every route
    that touches user data must depend on this, so real auth replaces only it.
    """
    user = session.exec(select(User).where(User.email == settings.dev_user_email)).first()
    if user is None:
        user = User(email=settings.dev_user_email, display_name=settings.dev_user_display_name)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user
