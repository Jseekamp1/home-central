from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

import app.routers.auth as auth_module
from app.main import app as fastapi_app


@pytest.fixture
def mock_supabase():
    mock = MagicMock()
    with patch.object(auth_module, "supabase", mock):
        yield mock


@pytest.fixture
def client(mock_supabase):
    return TestClient(fastapi_app)
