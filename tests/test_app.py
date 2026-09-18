from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"

    client.post(f"/activities/{activity}/signup?email={email}")

    response = client.delete(f"/activities/{activity}/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"

    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_participant_returns_404_if_missing():
    response = client.delete("/activities/Chess Club/participants/ghost@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
