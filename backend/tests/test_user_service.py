import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.user_service import (
    create_user,
    delete_user,
    get_user,
    list_users,
    update_user,
)


@pytest.fixture
def base_user(db_session: Session) -> User:
    return create_user(
        session=db_session,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pw",
    )


# --- List Users
def test_list_users_returns_empty_when_no_users(db_session: Session):
    assert list_users(db_session) == []


def test_list_users_returns_single_user(db_session: Session, base_user: User):
    assert list_users(db_session) == [base_user]


def test_list_users_returns_multiple_users(db_session: Session):
    count = 5
    users = [
        create_user(db_session, f"user{i}@example.com", f"user{i}", "hashed_pw")
        for i in range(count)
    ]

    result = list_users(db_session)

    assert len(result) == count
    assert all(user in result for user in users)


# --- Get User
def test_get_user_returns_correct_user(db_session: Session, base_user: User):
    user = get_user(db_session, base_user.id)
    assert user.id == base_user.id
    assert user.email == base_user.email
    assert user.username == base_user.username


def test_get_user_raises_on_not_found(db_session: Session):
    with pytest.raises(NoResultFound):
        get_user(db_session, 999)


# --- Create User
def test_create_user(db_session: Session):
    user = create_user(
        session=db_session,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pw",
    )

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.hashed_password == "hashed_pw"
    assert user.created_at is not None


def test_create_user_persists_to_database(db_session: Session):
    user = create_user(db_session, "test@example.com", "testuser", "hashed_pw")
    assert list_users(db_session) == [user]


def test_create_user_raises_on_duplicate_email(db_session: Session, base_user: User):
    with pytest.raises(IntegrityError):
        create_user(db_session, "test@example.com", "other", "hashed_pw")


def test_create_user_raises_on_duplicate_username(db_session: Session, base_user: User):
    with pytest.raises(IntegrityError):
        create_user(db_session, "other@example.com", "testuser", "hashed_pw")


# --- Update User
def test_update_user_email(db_session: Session, base_user: User):
    updated = update_user(db_session, base_user.id, email="new@example.com")
    assert updated.email == "new@example.com"


def test_update_user_username(db_session: Session, base_user: User):
    updated = update_user(db_session, base_user.id, username="newusername")
    assert updated.username == "newusername"


def test_update_user_hashed_password(db_session: Session, base_user: User):
    updated = update_user(db_session, base_user.id, hashed_password="new_hashed_pw")
    assert updated.hashed_password == "new_hashed_pw"


def test_update_user_ignores_none_fields(db_session: Session, base_user: User):
    updated = update_user(
        db_session, base_user.id, email="new@example.com", username=None
    )
    assert updated.email == "new@example.com"
    assert updated.username == base_user.username
    assert updated.hashed_password == base_user.hashed_password


def test_update_user_persists_to_database(db_session: Session, base_user: User):
    update_user(db_session, base_user.id, email="new@example.com")
    user = get_user(db_session, base_user.id)
    assert user.email == "new@example.com"


def test_update_user_raises_on_not_found(db_session: Session):
    with pytest.raises(NoResultFound):
        update_user(db_session, 999, email="new@example.com")


# --- Delete User
def test_delete_user(db_session: Session, base_user: User):
    delete_user(db_session, base_user.id)
    assert list_users(db_session) == []


def test_delete_user_raises_on_not_found(db_session: Session):
    with pytest.raises(NoResultFound):
        delete_user(db_session, 999)
