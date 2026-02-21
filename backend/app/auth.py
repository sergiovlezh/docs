import base64
import hashlib

import bcrypt


def _prepare_password(password: str) -> bytes:
    """Pre-hash password with SHA-256 to avoid bcrypt 72 byte limit.

    Args:
        password (str): Plain text password.

    Returns:
        str: Pre-hashed password.
    """
    return base64.b64encode(hashlib.sha256(password.encode()).digest())


def hash_password(password: str) -> str:
    """Hash a plain text password.

    Args:
        password (str): Plain text password.

    Returns:
        str: Hashed password.
    """
    return bcrypt.hashpw(_prepare_password(password), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password.

    Args:
        plain_password (str): Plain text password.
        hashed_password (str): Hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(_prepare_password(plain_password), hashed_password.encode())
