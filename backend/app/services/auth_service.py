import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.auth import verify_password
from app.models.user import User, UserToken


class AuthService:
    def __init__(self, session: Session):
        self._db = session

    def create_token(self, user: User) -> UserToken:
        """Create and return a new token for the user, replacing any existing one.

        Args:
            user (User): The user to create the token for.

        Returns:
            UserToken: The newly created token.
        """
        self._db.execute(delete(UserToken).where(UserToken.user_id == user.id))
        token = UserToken(token=str(uuid.uuid4()), user_id=user.id)
        self._db.add(token)
        self._db.commit()
        self._db.refresh(token)
        return token

    def get_user_by_token(self, token: str) -> User:
        """Return the user associated with the given token.

        Args:
            token (str): The token string.

        Returns:
            User: The associated user.

        Raises:
            NoResultFound: If the token does not exist.
        """
        result = self._db.execute(
            select(UserToken).where(UserToken.token == token)
        ).scalar_one()
        return result.user

    def authenticate_user(self, login: str, password: str) -> User:
        """Authenticate a user by email or username and password.

        Args:
            login (str): Email or username.
            password (str): Plain text password.

        Returns:
            User: The authenticated user.

        Raises:
            NoResultFound: If credentials are invalid.
        """
        user = self._db.execute(
            select(User).where((User.email == login) | (User.username == login))
        ).scalar_one_or_none()

        if user is None or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return user

    def delete_token(self, token: str) -> None:
        """Invalidate a token.

        Args:
            token (str): The token string to delete.

        Raises:
            NoResultFound: If the token does not exist.
        """
        self._db.execute(delete(UserToken).where(UserToken.token == token))
        self._db.commit()
