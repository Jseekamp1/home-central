"""Updates may leave a field out, but may not blank a required one."""

import pytest

HOME = {"name": "Our House", "kind": "home", "postal_code": "55401"}


@pytest.fixture
def ids(client):
    property_id = client.post("/properties", json=HOME).json()["id"]
    project_id = client.post(f"/properties/{property_id}/projects", json={"title": "Faucet"}).json()["id"]
    step_id = client.post(f"/projects/{project_id}/steps", json={"title": "A"}).json()["steps"][0]["id"]
    return {"property": property_id, "project": project_id, "step": step_id}


@pytest.mark.parametrize(
    ("path", "field"),
    [
        ("/properties/{property}", "name"),
        ("/properties/{property}", "kind"),
        ("/properties/{property}", "postal_code"),
        ("/projects/{project}", "title"),
        ("/projects/{project}", "priority"),
        ("/projects/{project}", "status"),
        ("/projects/{project}/steps/{step}", "title"),
        ("/projects/{project}/steps/{step}", "wait_after_minutes"),
        ("/projects/{project}/steps/{step}", "keep_with_next"),
        ("/projects/{project}/steps/{step}", "done"),
    ],
)
def test_null_for_a_required_field_is_rejected_cleanly(client, ids, path, field):
    response = client.patch(path.format(**ids), json={field: None})

    assert response.status_code == 422
    assert field in str(response.json()["detail"])


@pytest.mark.parametrize(
    ("path", "field"),
    [
        ("/properties/{property}", "notes"),
        ("/projects/{project}", "due_date"),
        ("/projects/{project}/steps/{step}", "estimated_minutes"),
    ],
)
def test_optional_fields_can_still_be_cleared(client, ids, path, field):
    assert client.patch(path.format(**ids), json={field: None}).status_code == 200
