import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(UTC)


class TableBase(SQLModel):
    """Columns every table has: UUID id plus created/updated timestamps."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now, sa_column_kwargs={"onupdate": utc_now})


def enum_column(enum_cls: type[Enum], **kwargs: Any) -> Column:
    """Store an enum as text with a CHECK constraint (portable to Postgres)."""
    return Column(
        SAEnum(
            enum_cls,
            native_enum=False,
            create_constraint=True,
            length=max(len(m.value) for m in enum_cls),
            values_callable=lambda cls: [m.value for m in cls],
            name=f"{enum_cls.__name__.lower()}_check",
        ),
        nullable=False,
        **kwargs,
    )
