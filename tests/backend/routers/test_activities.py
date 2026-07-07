from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient


sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from backend.routers import activities as activities_router


class FakeUpdateResult:
    def __init__(self, modified_count: int):
        self.modified_count = modified_count


class FakeActivitiesCollection:
    def __init__(self, activities: dict):
        self.activities = activities

    def find(self, query: dict):
        values = list(self.activities.values())

        day_filter = query.get("schedule_details.days")
        if day_filter:
            target_day = day_filter["$in"][0]
            values = [
                activity
                for activity in values
                if target_day in activity["schedule_details"]["days"]
            ]

        end_time_filter = query.get("schedule_details.end_time")
        if end_time_filter:
            threshold = end_time_filter["$lt"]
            values = [
                activity
                for activity in values
                if activity["schedule_details"]["end_time"] < threshold
            ]

        return [dict(activity) for activity in values]

    def find_one(self, query: dict):
        return self.activities.get(query.get("_id"))

    def update_one(self, query: dict, update: dict):
        activity = self.activities.get(query.get("_id"))
        if not activity:
            return FakeUpdateResult(0)

        push_payload = update.get("$push")
        if push_payload:
            for key, value in push_payload.items():
                if key not in activity:
                    activity[key] = []
                activity[key].append(value)

        pull_payload = update.get("$pull")
        if pull_payload:
            for key, value in pull_payload.items():
                if key in activity and value in activity[key]:
                    activity[key].remove(value)

        return FakeUpdateResult(1)

    def aggregate(self, pipeline):
        days = set()
        for activity in self.activities.values():
            for day in activity["schedule_details"]["days"]:
                days.add(day)
        return [{"_id": day} for day in sorted(days)]


class FakeTeachersCollection:
    def __init__(self, teachers: dict):
        self.teachers = teachers

    def find_one(self, query: dict):
        return self.teachers.get(query.get("_id"))


def _create_test_client_for_activities(activities_data: dict, teachers_data: dict) -> TestClient:
    activities_router.activities_collection = FakeActivitiesCollection(activities_data)
    activities_router.teachers_collection = FakeTeachersCollection(teachers_data)

    app = FastAPI()
    app.include_router(activities_router.router)
    return TestClient(app)


def test_get_activities_filters_by_day():
    # Description: This test verifies the activities endpoint filters by day.

    # Arrange
    client = _create_test_client_for_activities(
        {
            "Chess Club": {
                "_id": "Chess Club",
                "participants": ["a@school.edu"],
                "max_participants": 12,
                "schedule_details": {
                    "days": ["Monday"],
                    "start_time": "15:15",
                    "end_time": "16:45",
                },
            },
            "Drama Club": {
                "_id": "Drama Club",
                "participants": ["b@school.edu"],
                "max_participants": 20,
                "schedule_details": {
                    "days": ["Tuesday"],
                    "start_time": "15:30",
                    "end_time": "17:30",
                },
            },
        },
        {"teacher1": {"_id": "teacher1"}},
    )

    # Act
    response = client.get("/activities", params={"day": "Monday"})

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Drama Club" not in payload


def test_signup_returns_success_for_authenticated_teacher():
    # Description: This test verifies signup returns success for an authenticated teacher.

    # Arrange
    client = _create_test_client_for_activities(
        {
            "Chess Club": {
                "_id": "Chess Club",
                "participants": ["existing@school.edu"],
                "max_participants": 12,
                "schedule_details": {
                    "days": ["Monday"],
                    "start_time": "15:15",
                    "end_time": "16:45",
                },
            }
        },
        {"teacher1": {"_id": "teacher1"}},
    )

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "new@school.edu", "teacher_username": "teacher1"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up new@school.edu for Chess Club"


def test_get_activities_applies_end_time_filter_for_general_cases():
    # Description: This test verifies the general end-time filter behavior for non-boundary values.

    # Arrange
    client = _create_test_client_for_activities(
        {
            "Chess Club": {
                "_id": "Chess Club",
                "participants": ["a@school.edu"],
                "max_participants": 12,
                "schedule_details": {
                    "days": ["Monday"],
                    "start_time": "15:15",
                    "end_time": "16:45",
                },
            },
            "Debate Team": {
                "_id": "Debate Team",
                "participants": ["b@school.edu"],
                "max_participants": 12,
                "schedule_details": {
                    "days": ["Friday"],
                    "start_time": "15:30",
                    "end_time": "17:30",
                },
            },
        },
        {"teacher1": {"_id": "teacher1"}},
    )

    # Act
    response = client.get("/activities", params={"end_time": "17:00"})

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Debate Team" not in payload
