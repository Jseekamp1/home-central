"""Imports every table model so SQLModel.metadata is complete.

Alembic and the migration test import this module. Add each new feature's
table models here.
"""

from app.features.projects.models import Project
from app.features.properties.models import Property, PropertyMember
from app.features.steps.models import ProjectStep
from app.features.users.models import User

__all__ = ["Project", "ProjectStep", "Property", "PropertyMember", "User"]
