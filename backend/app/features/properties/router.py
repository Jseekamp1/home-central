import uuid

from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from app.features.properties.access import require_property_role
from app.features.properties.models import (
    MemberRole,
    Property,
    PropertyCreate,
    PropertyMember,
    PropertyRead,
    PropertyUpdate,
)
from app.features.users.models import User
from app.shared.db import get_session
from app.shared.dependencies import get_current_user

router = APIRouter()


def _read(property_: Property, role: MemberRole) -> PropertyRead:
    return PropertyRead.model_validate(property_, update={"my_role": role})


@router.get("", response_model=list[PropertyRead])
def list_properties(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[PropertyRead]:
    rows = session.exec(
        select(Property, PropertyMember.role)
        .join(PropertyMember, PropertyMember.property_id == Property.id)
        .where(PropertyMember.user_id == user.id)
        .order_by(Property.name)
    ).all()
    return [_read(property_, role) for property_, role in rows]


@router.post("", response_model=PropertyRead, status_code=status.HTTP_201_CREATED)
def create_property(
    body: PropertyCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> PropertyRead:
    property_ = Property.model_validate(body)
    session.add(property_)
    session.add(PropertyMember(property_id=property_.id, user_id=user.id, role=MemberRole.owner))
    session.commit()
    session.refresh(property_)
    return _read(property_, MemberRole.owner)


@router.get("/{property_id}", response_model=PropertyRead)
def get_property(
    property_id: uuid.UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> PropertyRead:
    property_, role = require_property_role(session, property_id, user, MemberRole.viewer)
    return _read(property_, role)


@router.patch("/{property_id}", response_model=PropertyRead)
def update_property(
    property_id: uuid.UUID,
    body: PropertyUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> PropertyRead:
    property_, role = require_property_role(session, property_id, user, MemberRole.editor)
    property_.sqlmodel_update(body.model_dump(exclude_unset=True))
    session.add(property_)
    session.commit()
    session.refresh(property_)
    return _read(property_, role)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(
    property_id: uuid.UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> None:
    property_, _ = require_property_role(session, property_id, user, MemberRole.owner)
    session.delete(property_)
    session.commit()
