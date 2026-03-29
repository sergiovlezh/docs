from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependencies import CurrentUser, UserSvc
from app.auth.exceptions import DuplicateEmailError, InvalidCredentialsError
from app.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenData,
    TokenResponse,
    UserResponse,
)
from app.auth.security import create_access_token

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(body: RegisterRequest, svc: UserSvc) -> UserResponse:
    try:
        return svc.create(email=body.email.lower(), password=body.password)
    except DuplicateEmailError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user",
        ) from None


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, svc: UserSvc) -> TokenResponse:
    try:
        user = svc.authenticate(email=body.email.lower(), password=body.password)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        ) from None

    token = create_access_token(user_id=user.id, email=user.email)

    return TokenResponse(access_token=token)


@router.get("/me", response_model=TokenData)
def me(current_user: CurrentUser) -> TokenData:
    return current_user


@router.post("/swagger-login", response_model=TokenResponse, include_in_schema=False)
def swagger_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    svc: UserSvc,
) -> TokenResponse:
    try:
        user = svc.authenticate(
            email=form_data.username.lower(), password=form_data.password
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        ) from None

    access_token = create_access_token(user_id=user.id, email=user.email)

    return TokenResponse(access_token=access_token)
