import pytest

from unittest.mock import Mock
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.core.database import get_session

from app.controller.student_controller import get_user


# -----------------------------
# MOCK SESSION
# -----------------------------
@pytest.fixture
def mock_session():
    return Mock(spec=Session)


# -----------------------------
# OVERRIDE AUTH
# -----------------------------
def override_auth():
    return {
        "id": 1,
        "username": "testuser",
        "permissions": [
            "user.read",
            "user.write",
            "user.delete"
        ]
    }


# -----------------------------
# CLIENT FIXTURE
# -----------------------------
@pytest.fixture
def client(mock_session):

    # DB override
    def override_get_session():
        return mock_session

    app.dependency_overrides[get_session] = override_get_session

    # AUTH override
    app.dependency_overrides[get_user] = override_auth

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()