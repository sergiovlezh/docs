from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.database import get_db
from app.models.user import User
from app.services.auth_service import AuthService
from app.services.user_service import UserService

# --- DB
db_dep = Annotated[Session, Depends(get_db)]


# --- User service
def get_user_service(session: db_dep) -> UserService:
    return UserService(session)


user_svc_dep = Annotated[UserService, Depends(get_user_service)]


# --- Auth service
def get_auth_service(session: db_dep) -> AuthService:
    return AuthService(session)


auth_svc_dep = Annotated[AuthService, Depends(get_auth_service)]


# --- Current user
def get_current_user(request: Request):
    return request.state.user


current_user_dep = Annotated[User, Depends(get_current_user)]
