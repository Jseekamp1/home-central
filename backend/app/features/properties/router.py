import uuid

from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from app.features.properties.access import require_property_role
from app.features.properties.models import (
    MemberRole,
    MyColorUpdate,
    Property,
    PropertyColor,
    PropertyCreate,
    PropertyMember,
    PropertyRead,
    PropertyUpdate,
)
from app.features.users.models import User
from app.shared.db import get_session
from app.shared.dependencies import get_current_user

router = APIRouter()


def _read(property_: Property, membership: PropertyMember) -> PropertyRead:
    return PropertyRead.model_validate(
        property_, update={"my_role": membership.role, "my_color": membership.color}
    )


def _first_unused_color(session: Session, user: User) -> PropertyColor:
    """The first palette color this user isn't using; once all are used, cycle by count."""
    used = session.exec(select(PropertyMember.color).where(PropertyMember.user_id == user.id)).all()
    palette = list(PropertyColor)
    for color in palette:
        if color not in used:
            return color
    return palette[len(used) % len(palette)]


@router.get("", response_model=list[PropertyRead])
def list_properties(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[PropertyRead]:
    rows = session.exec(
        select(Property, PropertyMember)
        .join(PropertyMember, PropertyMember.property_id == Property.id)
        .where(PropertyMember.user_id == user.id)
        .order_by(Property.name)
    ).all()
    return [_read(property_, membership) for property_, membership in rows]


@router.post("", response_model=PropertyRead, status_code=status.HTTP_201_CREATED)
def create_property(
    body: PropertyCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> PropertyRead:
    property_ = Property.model_validate(body)
    membership = PropertyMember(
        property_id=property_.id,
        user_id=user.id,
        role=MemberRole.owner,
        color=_first_unused_color(session, user),
    )
    session.add(property_)
    session.add(membership)
    session.commit()
    session.refresh(property_)
    session.refresh(membership)
    return _read(property_, membership)


@router.get("/{property_id}", response_model=PropertyRead)
def get_property(
    property_id: uuid.UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> PropertyRead:
    property_, membership = require_property_role(session, property_id, user, MemberRole.viewer)
    return _read(property_, membership)


@router.patch("/{property_id}", response_model=PropertyRead)
def update_property(
    property_id: uuid.UUID,
    body: PropertyUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> PropertyRead:
    property_, membership = require_property_role(session, property_id, user, MemberRole.editor)
    property_.sqlmodel_update(body.model_dump(exclude_unset=True))
    session.add(property_)
    session.commit()
    session.refresh(property_)
    return _read(property_, membership)


@router.put("/{property_id}/my-color", response_model=PropertyRead)
def set_my_color(
    property_id: uuid.UUID,
    body: MyColorUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> PropertyRead:
    """Change the caller's own color for this property. Any member may do this."""
    property_, membership = require_property_role(session, property_id, user, MemberRole.viewer)
    membership.color = body.color
    session.add(membership)
    session.commit()
    session.refresh(membership)
    return _read(property_, membership)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(
    property_id: uuid.UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> None:
    property_, _ = require_property_role(session, property_id, user, MemberRole.owner)
    session.delete(property_)
    session.commit()
