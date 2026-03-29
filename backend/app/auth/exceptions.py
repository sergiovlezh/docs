class AuthError(Exception):
    """Base exception for auth-related errors."""


class InvalidCredentialsError(AuthError):
    """Raised when login credentials are invalid."""


class InvalidTokenError(AuthError):
    """Raised when a JWT token cannot be decoded or is missing claims."""


class DuplicateEmailError(AuthError):
    """Raised when attempting to register an already-used email."""
