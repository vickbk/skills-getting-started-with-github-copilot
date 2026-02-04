def test_add_user_to_activity():
    activity = "Programming Class"
    email = "newuser@example.com"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister?email={email}")
    # Add user
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_duplicate_activity_registration():
    activity = "Programming Class"
    email = "dupuser@example.com"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister?email={email}")
    # Add user
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Try to add again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a test activity and email
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister?email={email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

    # Unregister again should fail
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
