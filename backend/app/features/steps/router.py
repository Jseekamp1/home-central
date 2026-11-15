"""Steps belong to a project. Every change returns the whole project, so the
caller sees step positions, the project's summary and any status change at once."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, func, select

from app.features.projects.access import require_project_role
from app.features.projects.models import Project, ProjectDetail, ProjectStatus
from app.features.projects.read import steps_of, to_detail
from app.features.properties.models import MemberRole
from app.features.steps.models import ProjectStep, StepCreate, StepOrder, StepUpdate
from app.features.users.models import User
from app.shared.db import get_session
from app.shared.dependencies import get_current_user

router = APIRouter(prefix="/projects/{project_id}/steps")

# Checking off a step on a project that hasn't started yet means it has started.
_NOT_STARTED = (ProjectStatus.draft, ProjectStatus.ready)


def _step_or_404(session: Session, project: Project, step_id: uuid.UUID) -> ProjectStep:
    step = session.get(ProjectStep, step_id)
    if step is None or step.project_id != project.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Step not found")
    return step


def _renumber(session: Session, steps: list[ProjectStep]) -> None:
    for position, step in enumerate(steps, start=1):
        if step.position != position:
            step.position = position
            session.add(step)


@router.post("", response_model=ProjectDetail, status_code=status.HTTP_201_CREATED)
def add_step(
    project_id: uuid.UUID,
    body: StepCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> ProjectDetail:
    project, membership = require_project_role(session, project_id, user, MemberRole.editor)
    last = session.exec(select(func.max(ProjectStep.position)).where(ProjectStep.project_id == project.id)).one()
    session.add(ProjectStep.model_validate(body, update={"project_id": project.id, "position": (last or 0) + 1}))
    session.commit()
    return to_detail(session, project, membership.role)


@router.patch("/{step_id}", response_model=ProjectDetail)
def update_step(
    project_id: uuid.UUID,
    step_id: uuid.UUID,
    body: StepUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> ProjectDetail:
    project, membership = require_project_role(session, project_id, user, MemberRole.editor)
    step = _step_or_404(session, project, step_id)
    changes = body.model_dump(exclude_unset=True)

    done = changes.pop("done", None)
    if done is True and step.done_at is None:
        step.done_at = datetime.now(UTC)
        if project.status in _NOT_STARTED:
            project.status = ProjectStatus.in_progress
            session.add(project)
    elif done is False:
        # Un-checking a step never changes the project's status.
        step.done_at = None

    step.sqlmodel_update(changes)
    session.add(step)
    session.commit()
    session.refresh(project)
    return to_detail(session, project, membership.role)


@router.delete("/{step_id}", response_model=ProjectDetail)
def delete_step(
    project_id: uuid.UUID,
    step_id: uuid.UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> ProjectDetail:
    project, membership = require_project_role(session, project_id, user, MemberRole.editor)
    step = _step_or_404(session, project, step_id)
    session.delete(step)
    session.flush()
    _renumber(session, steps_of(session, project.id))
    session.commit()
    return to_detail(session, project, membership.role)


@router.put("/order", response_model=ProjectDetail)
def reorder_steps(
    project_id: uuid.UUID,
    body: StepOrder,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> ProjectDetail:
    project, membership = require_project_role(session, project_id, user, MemberRole.editor)
    steps = steps_of(session, project.id)
    by_id = {step.id: step for step in steps}

    if len(body.step_ids) != len(set(body.step_ids)) or set(body.step_ids) != set(by_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "List every step of this project exactly once, in the new order.",
        )

    _renumber(session, [by_id[step_id] for step_id in body.step_ids])
    session.commit()
    return to_detail(session, project, membership.role)
