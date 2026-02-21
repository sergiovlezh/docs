from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.user_service import UserService

# --- DB
db_dep = Annotated[Session, Depends(get_db)]


# --- User service
def get_user_service(session: db_dep) -> UserService:
    return UserService(session)


user_svc_dep = Annotated[UserService, Depends(get_user_service)]
