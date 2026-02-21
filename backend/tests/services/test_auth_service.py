import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models.user import User
from app.services.auth_service import AuthService
from app.services.user_service import UserService


@pytest.fixture
def user_service(db_session: Session) -> UserService:
    return UserService(db_session)


@pytest.fixture
def service(db_session: Session) -> AuthService:
    return AuthService(db_session)


@pytest.fixture
def base_user(user_service: UserService) -> User:
    return user_service.create_user(
        email="test@example.com",
        username="testuser",
        hashed_password=hash_password("password123"),
    )


# --- Register user
def test_register_user_returns_token(service: AuthService):
    token = service.register_user("new@example.com", "newuser", "password123")

    assert token is not None
    assert isinstance(token, str)


def test_register_user_token_is_valid(service: AuthService):
    token = service.register_user("new@example.com", "newuser", "password123")
    user = service.get_authenticated_user(token)

    assert user is not None
    assert user.email == "new@example.com"


def test_register_user_raises_on_duplicate_email(service: AuthService):
    service.register_user("test@example.com", "testuser", "password123")

    with pytest.raises(IntegrityError):
        service.register_user("test@example.com", "other", "password123")


def test_register_user_raises_on_duplicate_username(service: AuthService):
    service.register_user("test@example.com", "testuser", "password123")

    with pytest.raises(IntegrityError):
        service.register_user("other@example.com", "testuser", "password123")


# --- Authentication
def test_login_user_with_email(service: AuthService, base_user: User):
    token = service.login_user("test@example.com", "password123")
    user = service.get_authenticated_user(token)

    assert user.id == base_user.id


def test_login_user_with_username(service: AuthService, base_user: User):
    token = service.login_user("testuser", "password123")
    user = service.get_authenticated_user(token)

    assert user.id == base_user.id


def test_login_user_raises_on_wrong_password(service: AuthService, base_user: User):
    with pytest.raises(ValueError):
        service.login_user("test@example.com", "wrongpassword")


def test_login_user_raises_on_unknown_login(service: AuthService):
    with pytest.raises(ValueError):
        service.login_user("nobody@example.com", "password123")


def test_get_authenticated_user_returns_valid_token(
    service: AuthService, base_user: User
):
    token = service.login_user("test@example.com", "password123")
    user = service.get_authenticated_user(token)

    assert user.id == base_user.id


def test_get_authenticated_user_returns_none_on_invalid_token(service: AuthService):
    user = service.get_authenticated_user("invalid-token")

    assert user is None


# --- Delete token
def test_logout_user_invalidates_token(service: AuthService, base_user: User):
    token = service.login_user("test@example.com", "password123")
    service.logout_user(token)

    assert service.get_authenticated_user(token) is None


def test_logout_user_is_silent_on_missing_token(service: AuthService):
    service.logout_user("nonexistent-token")
