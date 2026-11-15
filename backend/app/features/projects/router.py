import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import case
from sqlmodel import Session, select

from app.features.projects.access import require_project_role
from app.features.projects.models import (
    ACTIVE_STATUSES,
    Project,
    ProjectCreate,
    ProjectDetail,
    ProjectPriority,
    ProjectRead,
    ProjectStatus,
    ProjectUpdate,
    ProjectView,
)
from app.features.projects.read import step_summaries, to_detail, to_read, to_reads
from app.features.properties.access import require_property_role
from app.features.properties.models import MemberRole, PropertyMember
from app.features.users.models import User
from app.shared.db import get_session
from app.shared.dependencies import get_current_user

router = APIRouter()

_PRIORITY_ORDER = case(
    {ProjectPriority.urgent: 0, ProjectPriority.high: 1, ProjectPriority.medium: 2, ProjectPriority.low: 3},
    value=Project.priority,
)


def _list(session: Session, user: User, view: ProjectView, property_id: uuid.UUID | None = None):
    """Projects the user can see, filtered by view and ordered for that view."""
    query = (
        select(Project, PropertyMember.role)
        .join(PropertyMember, PropertyMember.property_id == Project.property_id)
        .where(PropertyMember.user_id == user.id)
    )
    if property_id is not None:
        query = query.where(Project.property_id == property_id)

    if view == ProjectView.active:
        query = query.where(Project.status.in_(ACTIVE_STATUSES)).order_by(
            _PRIORITY_ORDER,
            Project.due_date.is_(None),  # projects without a due date go last
            Project.due_date,
            Project.created_at.desc(),
        )
    elif view == ProjectView.done:
        query = query.where(Project.status == ProjectStatus.done).order_by(Project.completed_at.desc())
    else:
        query = query.where(Project.status == ProjectStatus.cancelled).order_by(Project.updated_at.desc())

    return to_reads(session, list(session.exec(query).all()))


def _ready_problem(session: Session, project: Project) -> str | None:
    """Why a project can't be marked ready yet, or None if it can.

    A ready project can be scheduled, so it needs at least one step and every
    step needs a time estimate.
    """
    summary = step_summaries(session, [project.id]).get(project.id)
    if not summary or summary["step_count"] == 0:
        return "Add at least one step, with a time estimate, before marking it ready."
    missing = summary["unestimated_step_count"]
    if missing:
        noun = "step needs" if missing == 1 else "steps need"
        return f"{missing} {noun} a time estimate before it's ready."
    return None


@router.get("/projects", response_model=list[ProjectRead])
def list_all_projects(
    view: ProjectView = ProjectView.active,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[ProjectRead]:
    """Every project across all the user's properties (the All properties view)."""
    return _list(session, user, view)


@router.get("/properties/{property_id}/projects", response_model=list[ProjectRead])
def list_property_projects(
    property_id: uuid.UUID,
    view: ProjectView = ProjectView.active,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[ProjectRead]:
    require_property_role(session, property_id, user, MemberRole.viewer)
    return _list(session, user, view, property_id)


@router.post(
    "/properties/{property_id}/projects",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    property_id: uuid.UUID,
    body: ProjectCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> ProjectRead:
    _, membership = require_property_role(session, property_id, user, MemberRole.editor)
    project = Project.model_validate(body, update={"property_id": property_id})
    session.add(project)
    session.commit()
    session.refresh(project)
    return to_read(session, project, membership.role)


@router.get("/projects/{project_id}", response_model=ProjectDetail)
def get_project(
    project_id: uuid.UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> ProjectDetail:
    project, membership = require_project_role(session, project_id, user, MemberRole.viewer)
    return to_detail(session, project, membership.role)


@router.patch("/projects/{project_id}", response_model=ProjectDetail)
def update_project(
    project_id: uuid.UUID,
    body: ProjectUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> ProjectDetail:
    project, membership = require_project_role(session, project_id, user, MemberRole.editor)
    changes = body.model_dump(exclude_unset=True)

    new_status = changes.get("status")
    if new_status == ProjectStatus.ready and project.status != ProjectStatus.ready:
        problem = _ready_problem(session, project)
        if problem:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, problem)
    if new_status is not None and new_status != project.status:
        project.completed_at = datetime.now(UTC) if new_status == ProjectStatus.done else None

    project.sqlmodel_update(changes)
    session.add(project)
    session.commit()
    session.refresh(project)
    return to_detail(session, project, membership.role)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: uuid.UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> None:
    project, _ = require_project_role(session, project_id, user, MemberRole.editor)
    session.delete(project)
    session.commit()
