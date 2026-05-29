"""Tests for the activities API endpoints using AAA (Arrange-Act-Assert) pattern."""

from urllib.parse import quote


def test_get_activities(client):
    # Arrange

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    encoded = quote(activity, safe="")

    # Act
    resp = client.post(f"/activities/{encoded}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert "Signed up" in resp.json()["message"]

    # Verify participant present
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already signed up in seed data
    encoded = quote(activity, safe="")

    # Act
    resp = client.post(f"/activities/{encoded}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]


def test_unregister_from_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    encoded = quote(activity, safe="")

    # Act
    resp = client.post(f"/activities/{encoded}/unregister", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert "Unregistered" in resp.json()["message"]

    # Verify removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_not_signed_up(client):
    # Arrange
    activity = "Art Club"
    email = "notstudent@mergington.edu"
    encoded = quote(activity, safe="")

    # Act
    resp = client.post(f"/activities/{encoded}/unregister", params={"email": email})

    # Assert
    assert resp.status_code == 400
    assert "not signed up" in resp.json()["detail"]


def test_activity_not_found_signup(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    encoded = quote(activity, safe="")

    # Act
    resp = client.post(f"/activities/{encoded}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"]


def test_activity_not_found_unregister(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    encoded = quote(activity, safe="")

    # Act
    resp = client.post(f"/activities/{encoded}/unregister", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"]
