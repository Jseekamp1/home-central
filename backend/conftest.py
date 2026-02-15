from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

import app.features.auth.router as auth_router_module
import app.shared.dependencies as dependencies_module
from app.main import app as fastapi_app


@pytest.fixture
def mock_supabase():
    mock = MagicMock()
    with patch.object(auth_router_module, "supabase", mock), \
         patch.object(dependencies_module, "supabase", mock), \
         patch.object(dependencies_module, "create_client", return_value=mock):
        yield mock


@pytest.fixture
def client(mock_supabase):
    return TestClient(fastapi_app)
