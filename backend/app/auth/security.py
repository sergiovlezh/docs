import uuid
from datetime import UTC, datetime, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.auth.exceptions import InvalidTokenError
from app.auth.schemas import TokenData
from app.core.config import settings

password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def hash_password(plain: str) -> str:
    """Hash a plaintext password using Argon2.

    Args:
        plain (str): The plaintext password to hash.

    Returns:
        str: The resulting hash string.
    """
    return password_hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against a hashed password.

    Args:
        plain (str): The plaintext password to verify.
        hashed (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    try:
        return password_hasher.verify(hashed, plain)
    except VerifyMismatchError:
        return False


def create_access_token(user_id: uuid.UUID, email: str) -> str:
    """Create a JWT access token for a user.

    Args:
        user_id (uuid.UUID): The user's unique identifier.
        email (str): The user's email address.

    Returns:
        str: A JWT access token as a string.
    """
    expire = datetime.now(UTC) + timedelta(hours=settings.TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> TokenData:
    """Decode a JWT access token and return the token data.

    Args:
        token (str): The JWT access token to decode.

    Returns:
        TokenData: The decoded token data.

    Raises:
        InvalidTokenError: If the token is invalid or missing claims.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str | None = payload.get("sub")
        email: str | None = payload.get("email")
        if user_id is None or email is None:
            raise InvalidTokenError("Missing claims in token")
        return TokenData(user_id=uuid.UUID(user_id), email=email)
    except jwt.PyJWTError as err:
        raise InvalidTokenError("Could not decode token") from err
