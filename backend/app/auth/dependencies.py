from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.exceptions import InvalidTokenError
from app.auth.schemas import TokenData
from app.auth.security import decode_access_token
from app.auth.service import UserService
from app.core.database import get_db

# tokenUrl only tells Swagger UI where to send the login form;
# it does not affect how protected endpoints validate Bearer tokens.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/swagger-login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    try:
        return decode_access_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


def get_user_service(db: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(db)


CurrentUser = Annotated[TokenData, Depends(get_current_user)]
UserSvc = Annotated[UserService, Depends(get_user_service)]
