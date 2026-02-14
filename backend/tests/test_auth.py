from unittest.mock import MagicMock

from supabase_auth.errors import AuthApiError


class TestSignup:
    def test_signup_success(self, client, mock_supabase):
        mock_user = MagicMock()
        mock_user.id = "user-123"
        mock_user.email = "test@example.com"

        mock_session = MagicMock()
        mock_session.access_token = "token-abc"

        mock_response = MagicMock()
        mock_response.user = mock_user
        mock_response.session = mock_session

        mock_supabase.auth.sign_up.return_value = mock_response

        resp = client.post(
            "/auth/signup",
            json={"email": "test@example.com", "password": "securepass123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["user"]["id"] == "user-123"
        assert data["user"]["email"] == "test@example.com"
        assert data["session"]["access_token"] == "token-abc"

    def test_signup_duplicate_email(self, client, mock_supabase):
        mock_supabase.auth.sign_up.side_effect = AuthApiError(
            "User already registered", 400, code=None
        )

        resp = client.post(
            "/auth/signup",
            json={"email": "existing@example.com", "password": "securepass123"},
        )
        assert resp.status_code == 400
        assert "already registered" in resp.json()["detail"].lower()


class TestLogin:
    def test_login_success(self, client, mock_supabase):
        mock_user = MagicMock()
        mock_user.id = "user-123"
        mock_user.email = "test@example.com"

        mock_session = MagicMock()
        mock_session.access_token = "token-abc"

        mock_response = MagicMock()
        mock_response.user = mock_user
        mock_response.session = mock_session

        mock_supabase.auth.sign_in_with_password.return_value = mock_response

        resp = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "securepass123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["session"]["access_token"] == "token-abc"
        assert data["user"]["email"] == "test@example.com"

    def test_login_bad_credentials(self, client, mock_supabase):
        mock_supabase.auth.sign_in_with_password.side_effect = AuthApiError(
            "Invalid login credentials", 401, code=None
        )

        resp = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "wrongpass"},
        )
        assert resp.status_code == 401
        assert "invalid" in resp.json()["detail"].lower()


class TestMe:
    def test_me_with_valid_token(self, client, mock_supabase):
        mock_user = MagicMock()
        mock_user.id = "user-123"
        mock_user.email = "test@example.com"

        mock_response = MagicMock()
        mock_response.user = mock_user

        mock_supabase.auth.get_user.return_value = mock_response

        resp = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer valid-token"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == "user-123"
        assert data["email"] == "test@example.com"

    def test_me_without_token(self, client, mock_supabase):
        resp = client.get("/auth/me")
        assert resp.status_code == 401

    def test_me_with_invalid_token(self, client, mock_supabase):
        mock_supabase.auth.get_user.side_effect = AuthApiError(
            "Invalid token", 401, code=None
        )

        resp = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer bad-token"},
        )
        assert resp.status_code == 401
