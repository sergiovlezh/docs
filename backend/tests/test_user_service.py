import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.user_service import UserService


@pytest.fixture
def service(db_session: Session) -> UserService:
    return UserService(db_session)


@pytest.fixture
def base_user(service: UserService) -> User:
    return service.create_user(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pw",
    )


# --- List Users
def test_list_users_returns_empty_when_no_users(service: UserService):
    assert service.list_users() == []


def test_list_users_returns_single_user(service: UserService, base_user: User):
    assert service.list_users() == [base_user]


def test_list_users_returns_multiple_users(service: UserService):
    count = 5
    users = [
        service.create_user(
            email=f"user{i}@example.com",
            username=f"user{i}",
            hashed_password="hashed_pw",
        )
        for i in range(count)
    ]

    result = service.list_users()

    assert len(result) == count
    assert all(user in result for user in users)


# --- Get User
def test_get_user_returns_correct_user(service: UserService, base_user: User):
    user = service.get_user(base_user.id)
    assert user.id == base_user.id
    assert user.email == base_user.email
    assert user.username == base_user.username


def test_get_user_raises_on_not_found(service: UserService):
    with pytest.raises(NoResultFound):
        service.get_user(999)


# --- Create User
def test_create_user(service: UserService):
    user = service.create_user(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pw",
    )

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.hashed_password == "hashed_pw"
    assert user.created_at is not None


def test_create_user_persists_to_database(service: UserService):
    user = service.create_user(
        email="test@example.com", username="testuser", hashed_password="hashed_pw"
    )
    assert service.list_users() == [user]


def test_create_user_raises_on_duplicate_email(service: UserService):
    service.create_user(
        email="test@example.com", username="testuser", hashed_password="hashed_pw"
    )

    with pytest.raises(IntegrityError):
        service.create_user(
            email="test@example.com", username="testuser2", hashed_password="hashed_pw2"
        )


def test_create_user_raises_on_duplicate_username(service: UserService):
    service.create_user(
        email="test@example.com", username="testuser", hashed_password="hashed_pw"
    )

    with pytest.raises(IntegrityError):
        service.create_user(
            email="test2@example.com", username="testuser", hashed_password="hashed_pw2"
        )


# --- Update User
def test_update_user_email(service: UserService, base_user: User):
    updated = service.update_user(base_user.id, email="new@example.com")
    assert updated.email == "new@example.com"


def test_update_user_username(service: UserService, base_user: User):
    updated = service.update_user(base_user.id, username="newusername")
    assert updated.username == "newusername"


def test_update_user_hashed_password(service: UserService, base_user: User):
    updated = service.update_user(base_user.id, hashed_password="new_hashed_pw")
    assert updated.hashed_password == "new_hashed_pw"


def test_update_user_ignores_none_fields(service: UserService, base_user: User):
    updated = service.update_user(base_user.id, email="new@example.com", username=None)
    assert updated.email == "new@example.com"
    assert updated.username == base_user.username
    assert updated.hashed_password == base_user.hashed_password


def test_update_user_persists_to_database(service: UserService, base_user: User):
    service.update_user(base_user.id, email="new@example.com")
    user = service.get_user(base_user.id)
    assert user.email == "new@example.com"


def test_update_user_raises_on_not_found(service: UserService):
    with pytest.raises(NoResultFound):
        service.update_user(999, email="new@example.com")


# --- Delete User
def test_delete_user(service: UserService, base_user: User):
    service.delete_user(base_user.id)
    assert service.list_users() == []


def test_delete_user_raises_on_not_found(service: UserService):
    with pytest.raises(NoResultFound):
        service.delete_user(999)
