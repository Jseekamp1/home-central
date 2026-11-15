import uuid
from datetime import date, datetime
from enum import Enum
from typing import Annotated

from pydantic import StringConstraints
from sqlmodel import Field, SQLModel

from app.features.properties.models import MemberRole
from app.shared.table_base import TableBase, enum_column


class ProjectStatus(str, Enum):
    draft = "draft"
    ready = "ready"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"


class ProjectPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class ProjectView(str, Enum):
    active = "active"
    done = "done"
    cancelled = "cancelled"


ACTIVE_STATUSES = (ProjectStatus.draft, ProjectStatus.ready, ProjectStatus.in_progress)

Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Description = Annotated[str, StringConstraints(strip_whitespace=True, max_length=5000)]


class Project(TableBase, table=True):
    __tablename__ = "projects"

    property_id: uuid.UUID = Field(foreign_key="properties.id", ondelete="CASCADE", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    status: ProjectStatus = Field(default=ProjectStatus.draft, sa_column=enum_column(ProjectStatus))
    priority: ProjectPriority = Field(default=ProjectPriority.medium, sa_column=enum_column(ProjectPriority))
    due_date: date | None = None
    # A property member who will do the work; no UI until other users exist.
    assignee_id: uuid.UUID | None = Field(default=None, foreign_key="users.id", ondelete="SET NULL")
    completed_at: datetime | None = None


class ProjectCreate(SQLModel):
    title: Title
    description: Description | None = None
    priority: ProjectPriority = ProjectPriority.medium
    due_date: date | None = None


class ProjectUpdate(SQLModel):
    title: Title | None = None
    description: Description | None = None
    priority: ProjectPriority | None = None
    due_date: date | None = None
    status: ProjectStatus | None = None


class ProjectRead(SQLModel):
    id: uuid.UUID
    property_id: uuid.UUID
    title: str
    description: str | None
    status: ProjectStatus
    priority: ProjectPriority
    due_date: date | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    my_role: MemberRole
