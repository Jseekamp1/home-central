from unittest.mock import MagicMock


USER_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
PROJECT_ID = "11111111-2222-3333-4444-555555555555"

SAMPLE_INSTRUCTIONS = [
    {"step": 1, "text": "Turn off water supply"},
    {"step": 2, "text": "Remove old faucet"},
]

SAMPLE_MATERIALS = [
    {"name": "Moen faucet", "quantity": 1, "cost": 89.99, "owned": False},
    {"name": "Plumber's tape", "quantity": 1, "cost": 3.99, "owned": True},
]

SAMPLE_PROJECT = {
    "id": PROJECT_ID,
    "user_id": USER_ID,
    "title": "Replace kitchen faucet",
    "description": "Install new moen faucet",
    "status": "planning",
    "priority": "medium",
    "estimated_duration_hours": 2.0,
    "estimated_cost": 150.0,
    "instructions": SAMPLE_INSTRUCTIONS,
    "materials": SAMPLE_MATERIALS,
    "created_at": "2026-01-01T00:00:00+00:00",
    "updated_at": "2026-01-01T00:00:00+00:00",
}

AUTH_HEADER = {"Authorization": "Bearer valid-token"}


def _mock_auth(mock_supabase):
    mock_user = MagicMock()
    mock_user.id = USER_ID
    mock_user.email = "test@example.com"
    mock_response = MagicMock()
    mock_response.user = mock_user
    mock_supabase.auth.get_user.return_value = mock_response


def _mock_table_insert(mock_supabase, return_data):
    execute = MagicMock()
    execute.data = [return_data]
    mock_supabase.table.return_value.insert.return_value.execute.return_value = execute


def _mock_table_select(mock_supabase, return_data):
    execute = MagicMock()
    execute.data = return_data
    mock_supabase.table.return_value.select.return_value.execute.return_value = execute


def _mock_table_select_eq(mock_supabase, return_data):
    execute = MagicMock()
    execute.data = return_data
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = execute


def _mock_table_update_eq(mock_supabase, return_data):
    execute = MagicMock()
    execute.data = return_data
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = execute


def _mock_table_delete_eq(mock_supabase, return_data):
    execute = MagicMock()
    execute.data = return_data
    mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = execute


class TestCreateProject:
    def test_create_success(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_insert(mock_supabase, SAMPLE_PROJECT)

        resp = client.post(
            "/projects",
            json={"title": "Replace kitchen faucet", "description": "Install new moen faucet"},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == PROJECT_ID
        assert data["title"] == "Replace kitchen faucet"
        assert data["user_id"] == USER_ID

    def test_create_missing_title(self, client, mock_supabase):
        _mock_auth(mock_supabase)

        resp = client.post(
            "/projects",
            json={"description": "No title provided"},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 422

    def test_create_empty_title(self, client, mock_supabase):
        _mock_auth(mock_supabase)

        resp = client.post(
            "/projects",
            json={"title": ""},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 422

    def test_create_invalid_status(self, client, mock_supabase):
        _mock_auth(mock_supabase)

        resp = client.post(
            "/projects",
            json={"title": "Test", "status": "invalid_status"},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 422

    def test_create_negative_cost(self, client, mock_supabase):
        _mock_auth(mock_supabase)

        resp = client.post(
            "/projects",
            json={"title": "Test", "estimated_cost": -50},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 422

    def test_create_without_token(self, client, mock_supabase):
        resp = client.post(
            "/projects",
            json={"title": "Test"},
        )
        assert resp.status_code == 401

    def test_create_uses_defaults(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        default_project = {
            **SAMPLE_PROJECT,
            "status": "planning",
            "priority": "medium",
            "instructions": [],
            "materials": [],
        }
        _mock_table_insert(mock_supabase, default_project)

        resp = client.post(
            "/projects",
            json={"title": "Minimal project"},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "planning"
        assert data["priority"] == "medium"
        assert data["instructions"] == []
        assert data["materials"] == []

    def test_create_with_instructions_and_materials(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_insert(mock_supabase, SAMPLE_PROJECT)

        resp = client.post(
            "/projects",
            json={
                "title": "Replace kitchen faucet",
                "instructions": SAMPLE_INSTRUCTIONS,
                "materials": SAMPLE_MATERIALS,
            },
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["instructions"]) == 2
        assert data["instructions"][0]["step"] == 1
        assert data["instructions"][0]["text"] == "Turn off water supply"
        assert len(data["materials"]) == 2
        assert data["materials"][0]["name"] == "Moen faucet"
        assert data["materials"][0]["owned"] is False
        assert data["materials"][1]["owned"] is True

    def test_create_invalid_instruction_missing_text(self, client, mock_supabase):
        _mock_auth(mock_supabase)

        resp = client.post(
            "/projects",
            json={"title": "Test", "instructions": [{"step": 1}]},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 422

    def test_create_invalid_material_missing_name(self, client, mock_supabase):
        _mock_auth(mock_supabase)

        resp = client.post(
            "/projects",
            json={"title": "Test", "materials": [{"quantity": 1}]},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 422

    def test_create_invalid_material_negative_cost(self, client, mock_supabase):
        _mock_auth(mock_supabase)

        resp = client.post(
            "/projects",
            json={"title": "Test", "materials": [{"name": "Tape", "cost": -5}]},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 422


class TestListProjects:
    def test_list_returns_projects(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_select(mock_supabase, [SAMPLE_PROJECT])

        resp = client.get("/projects", headers=AUTH_HEADER)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["title"] == "Replace kitchen faucet"

    def test_list_empty(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_select(mock_supabase, [])

        resp = client.get("/projects", headers=AUTH_HEADER)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_without_token(self, client, mock_supabase):
        resp = client.get("/projects")
        assert resp.status_code == 401


class TestGetProject:
    def test_get_success(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_select_eq(mock_supabase, [SAMPLE_PROJECT])

        resp = client.get(f"/projects/{SAMPLE_PROJECT['id']}", headers=AUTH_HEADER)
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Replace kitchen faucet"
        assert data["id"] == PROJECT_ID

    def test_get_not_found(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_select_eq(mock_supabase, [])

        resp = client.get("/projects/nonexistent-id", headers=AUTH_HEADER)
        assert resp.status_code == 404

    def test_get_without_token(self, client, mock_supabase):
        resp = client.get(f"/projects/{SAMPLE_PROJECT['id']}")
        assert resp.status_code == 401


class TestUpdateProject:
    def test_update_success(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_select_eq(mock_supabase, [SAMPLE_PROJECT])
        updated = {**SAMPLE_PROJECT, "title": "Updated title", "status": "in_progress"}
        _mock_table_update_eq(mock_supabase, [updated])

        resp = client.patch(
            f"/projects/{SAMPLE_PROJECT['id']}",
            json={"title": "Updated title", "status": "in_progress"},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Updated title"
        assert data["status"] == "in_progress"

    def test_update_partial(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_select_eq(mock_supabase, [SAMPLE_PROJECT])
        updated = {**SAMPLE_PROJECT, "priority": "high"}
        _mock_table_update_eq(mock_supabase, [updated])

        resp = client.patch(
            f"/projects/{SAMPLE_PROJECT['id']}",
            json={"priority": "high"},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["priority"] == "high"
        assert data["title"] == SAMPLE_PROJECT["title"]

    def test_update_instructions_and_materials(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_select_eq(mock_supabase, [SAMPLE_PROJECT])
        new_instructions = [{"step": 1, "text": "New step one"}]
        new_materials = [{"name": "New item", "quantity": 2, "cost": 10.0, "owned": False}]
        updated = {**SAMPLE_PROJECT, "instructions": new_instructions, "materials": new_materials}
        _mock_table_update_eq(mock_supabase, [updated])

        resp = client.patch(
            f"/projects/{SAMPLE_PROJECT['id']}",
            json={"instructions": new_instructions, "materials": new_materials},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["instructions"]) == 1
        assert data["instructions"][0]["text"] == "New step one"
        assert len(data["materials"]) == 1
        assert data["materials"][0]["name"] == "New item"

    def test_update_not_found(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_select_eq(mock_supabase, [])

        resp = client.patch(
            "/projects/nonexistent-id",
            json={"title": "Updated"},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 404

    def test_update_invalid_status(self, client, mock_supabase):
        _mock_auth(mock_supabase)

        resp = client.patch(
            f"/projects/{SAMPLE_PROJECT['id']}",
            json={"status": "invalid_status"},
            headers=AUTH_HEADER,
        )
        assert resp.status_code == 422

    def test_update_without_token(self, client, mock_supabase):
        resp = client.patch(
            f"/projects/{SAMPLE_PROJECT['id']}",
            json={"title": "Updated"},
        )
        assert resp.status_code == 401


class TestDeleteProject:
    def test_delete_success(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_select_eq(mock_supabase, [SAMPLE_PROJECT])
        _mock_table_delete_eq(mock_supabase, [SAMPLE_PROJECT])

        resp = client.delete(f"/projects/{SAMPLE_PROJECT['id']}", headers=AUTH_HEADER)
        assert resp.status_code == 200
        assert resp.json()["message"] == "Project deleted"

    def test_delete_not_found(self, client, mock_supabase):
        _mock_auth(mock_supabase)
        _mock_table_select_eq(mock_supabase, [])

        resp = client.delete("/projects/nonexistent-id", headers=AUTH_HEADER)
        assert resp.status_code == 404

    def test_delete_without_token(self, client, mock_supabase):
        resp = client.delete(f"/projects/{SAMPLE_PROJECT['id']}")
        assert resp.status_code == 401
