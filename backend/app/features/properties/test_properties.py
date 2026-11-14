import uuid

import pytest
from sqlmodel import select

from app.features.properties.models import PropertyMember

HOME = {"name": "Our House", "kind": "home", "postal_code": "55401"}


def create_property(client, **overrides):
    return client.post("/properties", json={**HOME, **overrides})


def add_member(session, property_id, user, role):
    member = PropertyMember(property_id=uuid.UUID(property_id), user_id=user.id, role=role)
    session.add(member)
    session.commit()


def test_creator_becomes_owner_and_sees_it_listed(client):
    response = create_property(client)

    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Our House"
    assert created["my_role"] == "owner"

    listed = client.get("/properties").json()
    assert [p["id"] for p in listed] == [created["id"]]
    assert listed[0]["my_role"] == "owner"


@pytest.mark.parametrize("overrides", [
    {"name": "   "},
    {"postal_code": ""},
    {"kind": "castle"},
])
def test_invalid_property_is_rejected(client, overrides):
    assert create_property(client, **overrides).status_code == 422


def test_list_only_shows_properties_the_user_belongs_to(client, make_user, act_as):
    mine = create_property(client, name="Mine").json()

    act_as(make_user("mom@example.com"))
    create_property(client, name="Mom's House")

    names = [p["name"] for p in client.get("/properties").json()]
    assert names == ["Mom's House"]
    assert mine["id"] not in [p["id"] for p in client.get("/properties").json()]


# Who may do what to a property. A non-member gets 404 so the API never
# reveals that the property exists.
PERMISSIONS = {
    #             viewer, editor, owner, non-member
    "read":      (200,    200,    200,   404),
    "update":    (403,    200,    200,   404),
    "delete":    (403,    403,    204,   404),
}
ROLES = ["viewer", "editor", "owner", None]


@pytest.mark.parametrize("action", PERMISSIONS)
@pytest.mark.parametrize("role_index", range(len(ROLES)))
def test_property_permissions(client, session, make_user, act_as, action, role_index):
    role = ROLES[role_index]
    property_id = create_property(client).json()["id"]

    other = make_user("other@example.com")
    if role is not None:
        add_member(session, property_id, other, role)
    act_as(other)

    if action == "read":
        response = client.get(f"/properties/{property_id}")
    elif action == "update":
        response = client.patch(f"/properties/{property_id}", json={"name": "Renamed"})
    else:
        response = client.delete(f"/properties/{property_id}")

    assert response.status_code == PERMISSIONS[action][role_index]


def test_partial_update_changes_only_given_fields(client):
    property_id = create_property(client).json()["id"]

    response = client.patch(f"/properties/{property_id}", json={"notes": "Blue door"})

    assert response.status_code == 200
    assert response.json()["notes"] == "Blue door"
    assert response.json()["name"] == "Our House"


def test_deleting_a_property_removes_its_memberships(client, session, make_user):
    property_id = create_property(client).json()["id"]
    add_member(session, property_id, make_user("viewer@example.com"), "viewer")

    assert client.delete(f"/properties/{property_id}").status_code == 204

    assert client.get(f"/properties/{property_id}").status_code == 404
    session.expire_all()
    assert session.exec(select(PropertyMember)).all() == []
