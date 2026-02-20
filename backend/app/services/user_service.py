from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_users(session: Session) -> list[User]:
    return session.execute(select(User)).scalars().all()


def create_user(
    session: Session,
    email: str,
    username: str,
    hashed_password: str,
) -> User:
    user = User(email=email, username=username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.execute(select(User).where(User.email == email)).scalar_one_or_none()


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.execute(
        select(User).where(User.username == username)
    ).scalar_one_or_none()
