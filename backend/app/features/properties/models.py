import uuid
from enum import Enum
from typing import Annotated

from pydantic import StringConstraints
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from app.shared.table_base import TableBase, enum_column


class PropertyKind(str, Enum):
    home = "home"
    rental = "rental"
    family = "family"
    organization = "organization"
    other = "other"


class MemberRole(str, Enum):
    viewer = "viewer"
    editor = "editor"
    owner = "owner"


class PropertyColor(str, Enum):
    """Palette keys; the frontend maps them to colors (see specs/design.md).

    Order matters: a new property gets the first key its creator isn't using.
    """

    sky = "sky"
    teal = "teal"
    lime = "lime"
    violet = "violet"
    pink = "pink"
    coral = "coral"
    sand = "sand"
    slate = "slate"


Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
PostalCode = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=20)]
AddressLine = Annotated[str, StringConstraints(strip_whitespace=True, max_length=200)]
Notes = Annotated[str, StringConstraints(strip_whitespace=True, max_length=2000)]


class Property(TableBase, table=True):
    __tablename__ = "properties"

    name: str = Field(max_length=100)
    kind: PropertyKind = Field(sa_column=enum_column(PropertyKind))
    postal_code: str = Field(max_length=20)
    address_line: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=2000)


class PropertyMember(TableBase, table=True):
    __tablename__ = "property_members"
    __table_args__ = (UniqueConstraint("property_id", "user_id"),)

    property_id: uuid.UUID = Field(foreign_key="properties.id", ondelete="CASCADE", index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", ondelete="CASCADE", index=True)
    role: MemberRole = Field(sa_column=enum_column(MemberRole))
    # Each member's own color for this property; personal, not shared.
    color: PropertyColor = Field(default=PropertyColor.sky, sa_column=enum_column(PropertyColor))


class PropertyCreate(SQLModel):
    name: Name
    kind: PropertyKind
    postal_code: PostalCode
    address_line: AddressLine | None = None
    notes: Notes | None = None


class PropertyUpdate(SQLModel):
    name: Name | None = None
    kind: PropertyKind | None = None
    postal_code: PostalCode | None = None
    address_line: AddressLine | None = None
    notes: Notes | None = None


class PropertyRead(SQLModel):
    id: uuid.UUID
    name: str
    kind: PropertyKind
    postal_code: str
    address_line: str | None
    notes: str | None
    my_role: MemberRole
    my_color: PropertyColor


class MyColorUpdate(SQLModel):
    color: PropertyColor
