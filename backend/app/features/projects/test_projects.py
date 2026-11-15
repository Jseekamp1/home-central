import uuid

import pytest
from sqlmodel import select

from app.features.projects.models import Project
from app.features.properties.models import PropertyMember

HOME = {"name": "Our House", "kind": "home", "postal_code": "55401"}


def create_property(client, name="Our House"):
    return client.post("/properties", json={**HOME, "name": name}).json()["id"]


def create_project(client, property_id, **fields):
    body = {"title": "Replace kitchen faucet", **fields}
    return client.post(f"/properties/{property_id}/projects", json=body)


def add_member(session, property_id, user, role):
    session.add(PropertyMember(property_id=uuid.UUID(property_id), user_id=user.id, role=role))
    session.commit()


# Who may do what to a property's projects. Non-members get 404 throughout.
PERMISSIONS = {
    #            viewer, editor, owner, non-member
    "list":     (200,    200,    200,   404),
    "create":   (403,    201,    201,   404),
    "read":     (200,    200,    200,   404),
    "update":   (403,    200,    200,   404),
    "delete":   (403,    204,    204,   404),
}
ROLES = ["viewer", "editor", "owner", None]


@pytest.mark.parametrize("action", PERMISSIONS)
@pytest.mark.parametrize("role_index", range(len(ROLES)))
def test_project_permissions(client, session, make_user, act_as, action, role_index):
    role = ROLES[role_index]
    property_id = create_property(client)
    project_id = create_project(client, property_id).json()["id"]

    other = make_user("other@example.com")
    if role is not None:
        add_member(session, property_id, other, role)
    act_as(other)

    if action == "list":
        response = client.get(f"/properties/{property_id}/projects")
    elif action == "create":
        response = create_project(client, property_id, title="Clean gutters")
    elif action == "read":
        response = client.get(f"/projects/{project_id}")
    elif action == "update":
        response = client.patch(f"/projects/{project_id}", json={"title": "Renamed"})
    else:
        response = client.delete(f"/projects/{project_id}")

    assert response.status_code == PERMISSIONS[action][role_index]


def test_deleting_a_property_removes_its_projects(client, session):
    property_id = create_property(client)
    create_project(client, property_id)
    create_project(client, property_id, title="Clean gutters")

    assert client.delete(f"/properties/{property_id}").status_code == 204

    session.expire_all()
    assert session.exec(select(Project)).all() == []


def test_active_projects_are_ordered_by_priority_then_due_date(client):
    property_id = create_property(client)
    create_project(client, property_id, title="Paint bedroom", priority="low")
    create_project(client, property_id, title="Clean gutters", priority="medium", due_date="2026-11-20")
    create_project(client, property_id, title="Seal driveway", priority="medium")
    create_project(client, property_id, title="Fix porch railing", priority="urgent", due_date="2026-11-10")
    create_project(client, property_id, title="Replace faucet", priority="medium", due_date="2026-11-18")

    titles = [p["title"] for p in client.get(f"/properties/{property_id}/projects").json()]

    assert titles == ["Fix porch railing", "Replace faucet", "Clean gutters", "Seal driveway", "Paint bedroom"]


def test_all_properties_list_shows_only_your_properties_projects(client, make_user, act_as):
    home = create_property(client, "Our House")
    moms = create_property(client, "Mom's House")
    create_project(client, home, title="Replace faucet", priority="high")
    create_project(client, moms, title="Fix porch railing", priority="urgent")

    act_as(make_user("stranger@example.com"))
    stranger_home = create_property(client, "Elsewhere")
    create_project(client, stranger_home, title="Not yours")

    response = client.get("/projects")
    assert [p["title"] for p in response.json()] == ["Not yours"]


