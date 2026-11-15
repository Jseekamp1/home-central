"""Property access rules, shared by every feature that lives inside a property."""

import uuid

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.features.properties.models import MemberRole, Property, PropertyMember
from app.features.users.models import User

_RANK = {MemberRole.viewer: 0, MemberRole.editor: 1, MemberRole.owner: 2}


def require_property_role(
    session: Session,
    property_id: uuid.UUID,
    user: User,
    minimum: MemberRole,
) -> tuple[Property, PropertyMember]:
    """Return the property and the user's membership in it, or raise.

    Non-members get 404 so the API never reveals that a property exists.
    Members whose role is below `minimum` get 403.
    """
    row = session.exec(
        select(Property, PropertyMember)
        .join(PropertyMember, PropertyMember.property_id == Property.id)
        .where(Property.id == property_id, PropertyMember.user_id == user.id)
    ).first()

    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Property not found")

    property_, membership = row
    if _RANK[membership.role] < _RANK[minimum]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"A {membership.role.value} can't do this")

    return property_, membership
