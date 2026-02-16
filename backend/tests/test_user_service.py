import pytest  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_users,
)


async def test_create_user(db_session: AsyncSession):
    assert await get_users(db_session) == []

    user = await create_user(
        session=db_session,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pw",
    )

    assert await get_users(db_session) == [user]
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.created_at is not None


async def test_get_user_by_email(db_session: AsyncSession):
    await create_user(
        session=db_session,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pw",
    )

    user = await get_user_by_email(db_session, "test@example.com")
    assert user is not None
    assert user.username == "testuser"


async def test_get_user_by_username(db_session: AsyncSession):
    await create_user(
        session=db_session,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pw",
    )

    user = await get_user_by_username(db_session, "testuser")
    assert user is not None
    assert user.email == "test@example.com"


async def test_get_user_by_email_not_found(db_session: AsyncSession):
    user = await get_user_by_email(db_session, "notfound@example.com")
    assert user is None
