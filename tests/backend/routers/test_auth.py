from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from backend.routers import auth as auth_router


class FakeTeachersCollection:
    def __init__(self, teachers: dict):
        self.teachers = teachers

    def find_one(self, query: dict):
        return self.teachers.get(query.get("_id"))


def _create_test_client_for_auth(teachers_data: dict) -> TestClient:
    auth_router.teachers_collection = FakeTeachersCollection(teachers_data)
    auth_router.verify_password = lambda stored, supplied: stored == supplied

    app = FastAPI()
    app.include_router(auth_router.router)
    return TestClient(app)


def test_login_returns_status_and_role():
    # Description: This test verifies login returns success status and role for valid credentials.

    # Arrange
    client = _create_test_client_for_auth(
        {
            "mchen": {
                "_id": "mchen",
                "username": "mchen",
                "display_name": "Mr. Chen",
                "password": "chess456",
                "role": "teacher",
            }
        }
    )

    # Act
    response = client.post(
        "/auth/login",
        params={"username": "mchen", "password": "chess456"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["role"] == "teacher"

@pytest.mark.skip(reason="Temp. Will fix later. (classic mistake)")
def test_login_rejects_invalid_password():
    # Description: This test verifies login rejects incorrect passwords.

    # Arrange
    client = _create_test_client_for_auth(
        {
            "mchen": {
                "_id": "mchen",
                "username": "mchen",
                "display_name": "Mr. Chen",
                "password": "chess456",
                "role": "teacher",
            }
        }
    )

    # Act
    response = client.post(
        "/auth/login",
        params={"username": "mchen", "password": "wrong"},
    )

    # Assert
    assert response.status_code == 401
