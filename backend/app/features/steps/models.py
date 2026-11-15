import uuid
from datetime import datetime
from typing import Annotated

from pydantic import Field as PydanticField
from pydantic import StringConstraints
from sqlmodel import Field, SQLModel

from app.shared.table_base import TableBase

Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Details = Annotated[str, StringConstraints(strip_whitespace=True, max_length=2000)]
# Up to a week of minutes: generous, but catches typos like an extra few zeros.
Minutes = Annotated[int, PydanticField(ge=0, le=7 * 24 * 60)]


class ProjectStep(TableBase, table=True):
    __tablename__ = "project_steps"

    project_id: uuid.UUID = Field(foreign_key="projects.id", ondelete="CASCADE", index=True)
    # 1..N within the project, with no gaps.
    position: int
    title: str = Field(max_length=200)
    details: str | None = Field(default=None, max_length=2000)
    estimated_minutes: int | None = None
    # Scheduling rules (used from Milestone 6): time that must pass before the next
    # step, and whether the next step has to happen in the same session.
    wait_after_minutes: int = 0
    keep_with_next: bool = False
    done_at: datetime | None = None


class StepCreate(SQLModel):
    title: Title
    details: Details | None = None
    estimated_minutes: Minutes | None = None
    wait_after_minutes: Minutes = 0
    keep_with_next: bool = False


class StepUpdate(SQLModel):
    title: Title | None = None
    details: Details | None = None
    estimated_minutes: Minutes | None = None
    wait_after_minutes: Minutes | None = None
    keep_with_next: bool | None = None
    done: bool | None = None


class StepOrder(SQLModel):
    step_ids: list[uuid.UUID]


class StepRead(SQLModel):
    id: uuid.UUID
    position: int
    title: str
    details: str | None
    estimated_minutes: int | None
    wait_after_minutes: int
    keep_with_next: bool
    done_at: datetime | None
