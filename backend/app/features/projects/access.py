import uuid

from fastapi import HTTPException, status
from sqlmodel import Session

from app.features.projects.models import Project
from app.features.properties.access import require_property_role
from app.features.properties.models import MemberRole, PropertyMember
from app.features.users.models import User


def require_project_role(
    session: Session,
    project_id: uuid.UUID,
    user: User,
    minimum: MemberRole,
) -> tuple[Project, PropertyMember]:
    """Return the project and the user's membership in its property, or raise.

    Same rules as properties: 404 for anyone who isn't a member, 403 below `minimum`.
    """
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    try:
        _, membership = require_property_role(session, project.property_id, user, minimum)
    except HTTPException as exc:
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found") from exc
        raise
    return project, membership
