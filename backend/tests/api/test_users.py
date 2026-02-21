import pytest
from fastapi.testclient import TestClient

from app.api.users import router as users_router

# --- Helpers
BASE_URL = users_router.prefix


def create_user_payload(
    email="test@example.com",
    username="testuser",
    password="password123",
):
    return {"email": email, "username": username, "password": password}


@pytest.fixture
def base_user(client: TestClient):
    response = client.post(f"{BASE_URL}/", json=create_user_payload())
    return response.json()


# --- GET /v1/users/
def test_list_users_returns_200(client: TestClient):
    response = client.get(f"{BASE_URL}/")

    assert response.status_code == 200


def test_list_users_returns_empty_list(client: TestClient):
    response = client.get(f"{BASE_URL}/")

    data = response.json()
    assert isinstance(data, list)
    assert data == []


def test_list_users_returns_existing_users(client: TestClient, base_user):
    response = client.get(f"{BASE_URL}/")
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == base_user["id"]


# --- GET /v1/users/{user_id}
def test_get_user_returns_200(client: TestClient, base_user):
    response = client.get(f"{BASE_URL}/{base_user['id']}")

    assert response.status_code == 200


def test_get_user_returns_correct_data(client: TestClient, base_user):
    response = client.get(f"{BASE_URL}/{base_user['id']}")
    data = response.json()

    assert data["id"] == base_user["id"]
    assert data["email"] == base_user["email"]
    assert data["username"] == base_user["username"]
    assert "password" not in data
    assert "hashed_password" not in data


def test_get_user_returns_404_when_not_found(client: TestClient):
    response = client.get(f"{BASE_URL}/999")

    assert response.status_code == 404


# --- POST /v1/users/
def test_create_user_returns_201(client: TestClient):
    response = client.post(f"{BASE_URL}/", json=create_user_payload())

    assert response.status_code == 201


def test_create_user_returns_correct_data(client: TestClient):
    response = client.post(f"{BASE_URL}/", json=create_user_payload())
    data = response.json()

    assert data["id"] is not None
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "password" not in data
    assert "hashed_password" not in data


def test_create_user_returns_409_on_duplicate_email(client: TestClient):
    client.post(f"{BASE_URL}/", json=create_user_payload())

    response = client.post(f"{BASE_URL}/", json=create_user_payload(username="other"))

    assert response.status_code == 409


def test_create_user_returns_409_on_duplicate_username(client: TestClient):
    client.post(f"{BASE_URL}/", json=create_user_payload())

    response = client.post(
        f"{BASE_URL}/", json=create_user_payload(email="other@example.com")
    )

    assert response.status_code == 409


def test_create_user_returns_422_on_invalid_email(client: TestClient):
    response = client.post(f"{BASE_URL}/", json=create_user_payload(email="notanemail"))

    assert response.status_code == 422


# --- PATCH /v1/users/{user_id}
def test_update_user_returns_200(client: TestClient, base_user):
    response = client.patch(
        f"{BASE_URL}/{base_user['id']}", json={"email": "new@example.com"}
    )

    assert response.status_code == 200


def test_update_user_returns_correct_data(client: TestClient, base_user):
    response = client.patch(
        f"{BASE_URL}/{base_user['id']}", json={"email": "new@example.com"}
    )
    data = response.json()

    assert data["email"] == "new@example.com"
    assert data["username"] == base_user["username"]


def test_update_user_returns_404_when_not_found(client: TestClient):
    response = client.patch(f"{BASE_URL}/999", json={"email": "new@example.com"})

    assert response.status_code == 404


def test_update_user_returns_409_on_duplicate_email(client: TestClient, base_user):
    client.post(
        f"{BASE_URL}/",
        json=create_user_payload(email="other@example.com", username="other"),
    )

    response = client.patch(
        f"{BASE_URL}/{base_user['id']}", json={"email": "other@example.com"}
    )

    assert response.status_code == 409


# --- DELETE /v1/users/{user_id}
def test_delete_user_returns_204(client: TestClient, base_user):
    response = client.delete(f"{BASE_URL}/{base_user['id']}")

    assert response.status_code == 204


def test_delete_user_removes_user(client: TestClient, base_user):
    client.delete(f"{BASE_URL}/{base_user['id']}")

    response = client.get(f"{BASE_URL}/{base_user['id']}")

    assert response.status_code == 404


def test_delete_user_returns_404_when_not_found(client: TestClient):
    response = client.delete(f"{BASE_URL}/999")

    assert response.status_code == 404
