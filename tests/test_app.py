import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def chess_club_activity():
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]

    yield activity_name, original_participants

    activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_from_activity(client, chess_club_activity):
    # Arrange
    activity_name, _ = chess_club_activity
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in activities[activity_name]["participants"]
