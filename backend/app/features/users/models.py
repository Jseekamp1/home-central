import uuid

from sqlmodel import Field, SQLModel

from app.shared.table_base import TableBase


class UserRead(SQLModel):
    id: uuid.UUID
    email: str
    display_name: str


class User(TableBase, table=True):
    __tablename__ = "users"

    email: str = Field(max_length=320, unique=True, index=True)
    display_name: str = Field(max_length=100)
