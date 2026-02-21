from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserService:
    def __init__(self, session: Session):
        self._db = session

    def list_users(self) -> list[User]:
        """List all users.

        Args:
            session (Session): The database session.

        Returns:
            list[User]: A list of all users.
        """
        return self._db.execute(select(User)).scalars().all()

    def get_user(self, user_id: int) -> User:
        """Get a user by ID.

        Args:
            session (Session): Database session.
            user_id (int): ID of the user to retrieve.

        Returns:
            User: The matching user.

        Raises:
            NoResultFound: If no user with the given ID exists.
        """
        return self._db.execute(select(User).where(User.id == user_id)).scalar_one()

    def create_user(
        self,
        *,
        email: str,
        username: str,
        hashed_password: str,
    ) -> User:
        """Create and return a new user.

        Args:
            session (Session): Database session.
            email (str): User's email address.
            username (str): User's username.
            hashed_password (str): Already-hashed password.

        Returns:
            User: The newly created user.

        Raises:
            IntegrityError: If an user with the same email or username already exists.
        """
        user = User(email=email, username=username, hashed_password=hashed_password)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(
        self,
        user_id: int,
        *,
        email: str | None = None,
        username: str | None = None,
        hashed_password: str | None = None,
    ) -> User:
        """Update and return an existing user.

        Only provided fields are updated.

        Args:
            session (Session): Database session.
            user_id (int): ID of the user to update.
            email (str | None): User's email address.
            username (str | None): User's username.
            hashed_password (str | None): Already-hashed password.

        Raises:
            NoResultFound: If no user with the given ID exists.
        """
        user = self.get_user(user_id)

        if email is not None:
            user.email = email
        if username is not None:
            user.username = username
        if hashed_password is not None:
            user.hashed_password = hashed_password

        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> None:
        """Delete an existing user.

        Args:
            session (Session): Database session.
            user_id (int): ID of the user to update.

        Raises:
            NoResultFound: If no user with the given ID exists.
        """
        user = self.get_user(user_id)
        self._db.delete(user)
        self._db.commit()
