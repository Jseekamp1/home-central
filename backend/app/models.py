"""Imports every table model so SQLModel.metadata is complete.

Alembic and the migration test import this module. Add each new feature's
table models here.
"""

from app.features.users.models import User

__all__ = ["User"]
