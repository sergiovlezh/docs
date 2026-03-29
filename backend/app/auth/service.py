from sqlalchemy.orm import Session

from app.auth.exceptions import DuplicateEmailError, InvalidCredentialsError
from app.auth.models import User
from app.auth.security import hash_password, verify_password

# Dummy hash used to keep login timing constant when email is not found,
# preventing user enumeration via response-time differences.
_DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$GZvLsx7LA4H7/aQkmlem+g$dlam1Dx8SlLHQxGZ8lOh0DCyORvrKmaBikzfg8m37v8"  # noqa: E501


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User | None: The user object if found, None otherwise.
        """
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, password: str) -> User:
        """Create a new user with the given email and password.

        Args:
            email (str): The email address for the new user.
            password (str): The plaintext password for the new user.

        Returns:
            User: The newly created user object.

        Raises:
            DuplicateEmailError: If a user with the given email already exists.
        """
        if self.get_by_email(email):
            raise DuplicateEmailError(email)

        user = User(
            email=email,
            hashed_password=hash_password(password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def authenticate(self, email: str, password: str) -> User:
        """Authenticate a user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The plaintext password of the user.

        Returns:
            User: The authenticated user object.

        Raises:
            InvalidCredentialsError: If the email or password is incorrect.
        """
        user = self.get_by_email(email)
        hashed = user.hashed_password if user is not None else _DUMMY_HASH
        is_valid = verify_password(password, hashed)
        if user is None or not is_valid:
            raise InvalidCredentialsError

        return user
