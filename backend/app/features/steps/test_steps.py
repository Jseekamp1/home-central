import uuid

import pytest
from sqlmodel import select

from app.features.properties.models import PropertyMember
from app.features.steps.models import ProjectStep

HOME = {"name": "Our House", "kind": "home", "postal_code": "55401"}


def new_project(client, **fields):
    property_id = client.post("/properties", json=HOME).json()["id"]
    body = {"title": "Replace kitchen faucet", **fields}
    project = client.post(f"/properties/{property_id}/projects", json=body).json()
    return property_id, project["id"]


def add_step(client, project_id, title, minutes=None):
    body = {"title": title}
    if minutes is not None:
        body["estimated_minutes"] = minutes
    return client.post(f"/projects/{project_id}/steps", json=body)


def step_ids(client, project_id):
    return [s["id"] for s in client.get(f"/projects/{project_id}").json()["steps"]]


def test_project_summarises_progress_and_estimates(client):
    property_id, project_id = new_project(client)
    first = add_step(client, project_id, "Turn off water", 15).json()["steps"][0]["id"]
    add_step(client, project_id, "Remove old faucet", 30)
    add_step(client, project_id, "Clean the sink deck")
    client.patch(f"/projects/{project_id}/steps/{first}", json={"done": True})

    detail = client.get(f"/projects/{project_id}").json()
    listed = client.get(f"/properties/{property_id}/projects").json()[0]

    for project in (detail, listed):
        assert project["step_count"] == 3
        assert project["done_step_count"] == 1
        assert project["estimated_minutes"] == 45
        assert project["unestimated_step_count"] == 1


def test_ready_needs_every_step_estimated(client):
    _, project_id = new_project(client)
    add_step(client, project_id, "Turn off water", 15)
    unestimated = add_step(client, project_id, "Clean the sink deck").json()["steps"][1]["id"]

    refused = client.patch(f"/projects/{project_id}", json={"status": "ready"})
    assert refused.status_code == 422
    assert "1 step" in refused.json()["detail"]

    client.patch(f"/projects/{project_id}/steps/{unestimated}", json={"estimated_minutes": 10})
    allowed = client.patch(f"/projects/{project_id}", json={"status": "ready"})
    assert allowed.status_code == 200
    assert allowed.json()["status"] == "ready"


@pytest.mark.parametrize("starting_status", ["draft", "ready"])
def test_checking_off_a_step_starts_the_project(client, starting_status):
    _, project_id = new_project(client)
    step_id = add_step(client, project_id, "Turn off water", 15).json()["steps"][0]["id"]
    if starting_status == "ready":
        client.patch(f"/projects/{project_id}", json={"status": "ready"})

    response = client.patch(f"/projects/{project_id}/steps/{step_id}", json={"done": True})

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"
    assert response.json()["steps"][0]["done_at"] is not None


def test_unchecking_a_step_never_changes_the_status(client):
    _, project_id = new_project(client)
    step_id = add_step(client, project_id, "Turn off water", 15).json()["steps"][0]["id"]
    client.patch(f"/projects/{project_id}/steps/{step_id}", json={"done": True})
    client.patch(f"/projects/{project_id}", json={"status": "done"})

    response = client.patch(f"/projects/{project_id}/steps/{step_id}", json={"done": False})

    assert response.json()["status"] == "done"
    assert response.json()["steps"][0]["done_at"] is None


def test_reorder_sets_positions_in_the_new_order(client):
    _, project_id = new_project(client)
    for title in ["A", "B", "C"]:
        add_step(client, project_id, title)
    a, b, c = step_ids(client, project_id)

    response = client.put(f"/projects/{project_id}/steps/order", json={"step_ids": [c, a, b]})

    assert response.status_code == 200
    assert [(s["position"], s["title"]) for s in response.json()["steps"]] == [(1, "C"), (2, "A"), (3, "B")]


def test_reorder_must_list_exactly_the_projects_steps(client):
    _, project_id = new_project(client)
    for title in ["A", "B"]:
        add_step(client, project_id, title)
    a, b = step_ids(client, project_id)
    _, other_project = new_project(client, title="Other")
    foreign = add_step(client, other_project, "Elsewhere").json()["steps"][0]["id"]

    assert client.put(f"/projects/{project_id}/steps/order", json={"step_ids": [a]}).status_code == 422
    assert client.put(f"/projects/{project_id}/steps/order", json={"step_ids": [a, foreign]}).status_code == 422
    assert client.put(f"/projects/{project_id}/steps/order", json={"step_ids": [a, a]}).status_code == 422
    assert step_ids(client, project_id) == [a, b]


def test_deleting_a_project_removes_its_steps(client, session):
    _, project_id = new_project(client)
    add_step(client, project_id, "Turn off water")

    assert client.delete(f"/projects/{project_id}").status_code == 204

    session.expire_all()
    assert session.exec(select(ProjectStep)).all() == []


def test_viewers_can_see_steps_but_not_change_them(client, session, make_user, act_as):
    property_id, project_id = new_project(client)
    step_id = add_step(client, project_id, "Turn off water").json()["steps"][0]["id"]
    viewer = make_user("viewer@example.com")
    session.add(PropertyMember(property_id=uuid.UUID(property_id), user_id=viewer.id, role="viewer"))
    session.commit()
    act_as(viewer)

    assert len(client.get(f"/projects/{project_id}").json()["steps"]) == 1
    assert add_step(client, project_id, "Sneaky").status_code == 403
    assert client.patch(f"/projects/{project_id}/steps/{step_id}", json={"done": True}).status_code == 403
    assert client.delete(f"/projects/{project_id}/steps/{step_id}").status_code == 403
