from typing import ClassVar

from pydantic import model_validator
from sqlmodel import SQLModel


class PatchModel(SQLModel):
    """Base for PATCH bodies: every field is optional, so a caller sends only what changes.

    Leaving a field out means "don't touch it". Sending null means "clear it", which
    is only allowed for the fields named in `clearable`; null for anything else is
    rejected here rather than reaching the database.
    """

    clearable: ClassVar[frozenset[str]] = frozenset()

    @model_validator(mode="after")
    def _reject_null_for_required_fields(self):
        blanked = sorted(
            name
            for name in self.model_fields_set
            if getattr(self, name) is None and name not in self.clearable
        )
        if blanked:
            raise ValueError(f"These fields can't be empty: {', '.join(blanked)}")
        return self
