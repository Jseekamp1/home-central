"""Build project responses with their step summary (shared by projects and steps)."""

import uuid

from sqlalchemy import case, func
from sqlmodel import Session, select

from app.features.projects.models import Project, ProjectDetail, ProjectRead
from app.features.properties.models import MemberRole
from app.features.steps.models import ProjectStep, StepRead

_EMPTY = {"step_count": 0, "done_step_count": 0, "estimated_minutes": 0, "unestimated_step_count": 0}


def step_summaries(session: Session, project_ids: list[uuid.UUID]) -> dict[uuid.UUID, dict[str, int]]:
    """Step counts and estimate totals per project, in one query."""
    if not project_ids:
        return {}
    rows = session.exec(
        select(
            ProjectStep.project_id,
            func.count(ProjectStep.id),
            func.count(ProjectStep.done_at),
            func.coalesce(func.sum(ProjectStep.estimated_minutes), 0),
            func.sum(case((ProjectStep.estimated_minutes.is_(None), 1), else_=0)),
        )
        .where(ProjectStep.project_id.in_(project_ids))
        .group_by(ProjectStep.project_id)
    ).all()
    return {
        project_id: {
            "step_count": total,
            "done_step_count": done,
            "estimated_minutes": minutes,
            "unestimated_step_count": unestimated,
        }
        for project_id, total, done, minutes, unestimated in rows
    }


def to_reads(session: Session, rows: list[tuple[Project, MemberRole]]) -> list[ProjectRead]:
    summaries = step_summaries(session, [project.id for project, _ in rows])
    return [
        ProjectRead.model_validate(project, update={"my_role": role, **summaries.get(project.id, _EMPTY)})
        for project, role in rows
    ]


def to_read(session: Session, project: Project, role: MemberRole) -> ProjectRead:
    return to_reads(session, [(project, role)])[0]


def steps_of(session: Session, project_id: uuid.UUID) -> list[ProjectStep]:
    return list(
        session.exec(
            select(ProjectStep).where(ProjectStep.project_id == project_id).order_by(ProjectStep.position)
        ).all()
    )


def to_detail(session: Session, project: Project, role: MemberRole) -> ProjectDetail:
    steps = [StepRead.model_validate(step) for step in steps_of(session, project.id)]
    summary = to_read(session, project, role)
    return ProjectDetail.model_validate(summary, update={"steps": steps})
