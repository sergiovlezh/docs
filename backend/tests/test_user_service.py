from sqlalchemy.orm import Session

from app.services.user_service import (
    create_user,
    list_users,
)


def test_create_user(db_session: Session):
    assert get_users(db_session) == []

    user = create_user(
        session=db_session,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pw",
    )

    assert get_users(db_session) == [user]
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.created_at is not None


def test_get_user_by_email(db_session: Session):
    create_user(
        session=db_session,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pw",
    )

    user = get_user_by_email(db_session, "test@example.com")
    assert user is not None
    assert user.username == "testuser"


def test_get_user_by_username(db_session: Session):
    create_user(
        session=db_session,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pw",
    )

    user = get_user_by_username(db_session, "testuser")
    assert user is not None
    assert user.email == "test@example.com"


def test_get_user_by_email_not_found(db_session: Session):
    user = get_user_by_email(db_session, "notfound@example.com")
    assert user is None
