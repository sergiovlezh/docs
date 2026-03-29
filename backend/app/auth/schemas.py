import uuid
from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field

from app.core.config import settings


class TokenData(BaseModel):
    user_id: uuid.UUID
    email: str


# Requests
class RegisterRequest(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=settings.MIN_PASSWORD_LENGTH)]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Responses
class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}
