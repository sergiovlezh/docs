import random
import string
import uuid
from datetime import UTC, datetime, timedelta

import jwt
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.security import verify_password
from app.core.config import settings

TEST_EMAIL = "user@example.com"
TEST_PASSWORD = "securepass123"


def register_user(
    client: TestClient, email: str = TEST_EMAIL, password: str = TEST_PASSWORD
):
    return client.post("/auth/register", json={"email": email, "password": password})


def login_user(
    client: TestClient, email: str = TEST_EMAIL, password: str = TEST_PASSWORD
):
    return client.post("/auth/login", json={"email": email, "password": password})


def bearer_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


# Register
# --- User creation ---
def test_register_creates_user_in_db(client: TestClient, db_session: Session):
    register_user(client)

    user = db_session.query(User).filter(User.email == TEST_EMAIL).first()

    assert user is not None


def test_register_stores_email_lowercased(client: TestClient, db_session: Session):
    uppercase_email = "User@EXAMPLE.com"
    register_user(client, email=uppercase_email)

    user = db_session.query(User).filter(User.email == uppercase_email.lower()).first()

    assert user is not None


def test_register_hashes_password(client: TestClient, db_session: Session):
    register_user(client)

    user = db_session.query(User).filter(User.email == TEST_EMAIL).first()

    assert user.hashed_password != TEST_PASSWORD
    assert verify_password(TEST_PASSWORD, user.hashed_password)


# --- Validation ---
def test_register_rejects_duplicate_email(client: TestClient):
    register_user(client)

    response = register_user(client)

    assert response.status_code == 409


def test_register_rejects_too_short_password(client: TestClient):
    too_short_password = "".join(
        random.choices(
            string.ascii_letters + string.digits, k=settings.MIN_PASSWORD_LENGTH - 1
        )
    )

    response = register_user(client, password=too_short_password)

    assert response.status_code == 422


def test_register_rejects_invalid_email(client: TestClient):
    response = register_user(client, email="not-an-email")

    assert response.status_code == 422


# --- Response schema ---
def test_register_response_contains_id(client: TestClient):
    response = register_user(client)

    assert "id" in response.json()
    assert uuid.UUID(response.json()["id"])


def test_register_response_contains_email(client: TestClient):
    response = register_user(client)

    assert response.json()["email"] == TEST_EMAIL


def test_register_response_contains_created_at(client: TestClient):
    response = register_user(client)

    assert "created_at" in response.json()


def test_register_response_excludes_password(client: TestClient):
    response = register_user(client)

    assert "hashed_password" not in response.json()
    assert "password" not in response.json()


# Login
# --- Success ---
def test_login_returns_200(client: TestClient):
    register_user(client)

    response = login_user(client)

    assert response.status_code == 200


def test_login_returns_access_token(client: TestClient):
    register_user(client)

    response = login_user(client)

    assert "access_token" in response.json()


def test_login_returns_bearer_token_type(client: TestClient):
    register_user(client)

    response = login_user(client)

    assert response.json()["token_type"] == "bearer"


def test_login_token_contains_user_claims(client: TestClient):
    register_user(client)

    response = login_user(client)
    token = response.json()["access_token"]
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    assert payload["email"] == TEST_EMAIL
    assert "sub" in payload
    assert "exp" in payload


# --- Failure ---
def test_login_rejects_wrong_password(client: TestClient):
    register_user(client)

    response = login_user(client, password="wrongpassword")

    assert response.status_code == 401


def test_login_rejects_unknown_email(client: TestClient):
    response = login_user(client, email="unknown@example.com")

    assert response.status_code == 401


# Me
# --- Authenticated ---
def test_me_returns_user_email(client: TestClient):
    register_user(client)
    token = login_user(client).json()["access_token"]

    response = client.get("/auth/me", headers=bearer_header(token))

    assert response.json()["email"] == TEST_EMAIL


def test_me_returns_user_id(client: TestClient):
    register_user(client)
    token = login_user(client).json()["access_token"]

    response = client.get("/auth/me", headers=bearer_header(token))

    assert "user_id" in response.json()
    assert uuid.UUID(response.json()["user_id"])


# --- Unauthenticated ---
def test_me_rejects_missing_token(client: TestClient):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me_rejects_invalid_token(client: TestClient):
    response = client.get("/auth/me", headers=bearer_header("invalid-token"))

    assert response.status_code == 401


def test_me_rejects_expired_token(client: TestClient):
    payload = {
        "sub": str(uuid.uuid4()),
        "email": TEST_EMAIL,
        "exp": datetime.now(UTC) - timedelta(hours=1),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    response = client.get("/auth/me", headers=bearer_header(token))

    assert response.status_code == 401
