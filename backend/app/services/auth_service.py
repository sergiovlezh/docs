import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.auth import hash_password, verify_password
from app.models.user import User, UserToken
from app.services.user_service import UserService


class AuthService:
    def __init__(self, session: Session):
        self._db = session

    def _create_token(self, user: User) -> str:
        """Create and return a new token for the user, replacing any existing one.

        Args:
            user (User): The user to create the token for.

        Returns:
            str: The newly created token string.
        """
        self._db.execute(delete(UserToken).where(UserToken.user_id == user.id))
        user_token = UserToken(token=str(uuid.uuid4()), user_id=user.id)
        self._db.add(user_token)
        self._db.commit()
        self._db.refresh(user_token)
        return user_token.token

    def _delete_token(self, token: str) -> None:
        """Invalidate a token.

        Args:
            token (str): The token string to delete.

        Raises:
            NoResultFound: If the token does not exist.
        """
        self._db.execute(delete(UserToken).where(UserToken.token == token))
        self._db.commit()

    def _authenticate_user(self, login: str, password: str) -> User:
        """Verify credentials by email or username and password.

        Args:
            login (str): Email or username.
            password (str): Plain text password.

        Returns:
            User: The matching user.

        Raises:
            ValueError: If credentials are invalid.
        """
        user = self._db.execute(
            select(User).where((User.email == login) | (User.username == login))
        ).scalar_one_or_none()

        if user is None or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return user

    def get_authenticated_user(self, token: str) -> User | None:
        """Return the user associated with the token, or None if invalid.

        Args:
            token (str): The token string.

        Returns:
            User | None: The associated user, or None if token is invalid.
        """
        user_token = self._db.execute(
            select(UserToken).where(UserToken.token == token)
        ).scalar_one_or_none()
        return user_token.user if user_token else None

    def register_user(self, email: str, username: str, password: str) -> str:
        """Register a new user and return a token.

        Args:
            email (str): User's email address.
            username (str): User's username.
            password (str): Plain text password.

        Returns:
            str: The newly created token string.

        Raises:
            IntegrityError: If email or username already exists.
        """
        user = UserService(self._db).create_user(
            email=email,
            username=username,
            hashed_password=hash_password(password),
        )
        return self._create_token(user)

    def login_user(self, login: str, password: str) -> str:
        """Verify credentials and return a token.

        Args:
            login (str): Email or username.
            password (str): Plain text password.

        Returns:
            str: The newly created token string.

        Raises:
            ValueError: If credentials are invalid.
        """
        user = self._authenticate_user(login, password)
        return self._create_token(user)

    def logout_user(self, token: str) -> None:
        """Invalidate the token for the current user.

        Args:
            token (str): The token string to invalidate.
        """
        self._delete_token(token)
