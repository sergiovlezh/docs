from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.api.dependencies import user_svc_dep
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
)


@router.get("/", response_model=list[UserRead])
def list_users(service: user_svc_dep):
    return service.list_users()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: user_svc_dep):
    try:
        return service.get_user(user_id)
    except NoResultFound as nrfex:
        print(nrfex)
        raise HTTPException(status_code=404, detail="User not found") from None


@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, service: user_svc_dep):
    try:
        return service.create_user(
            email=user.email,
            username=user.username,
            hashed_password=user.password,
        )
    except IntegrityError as ieex:
        print(ieex)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already exists",
        ) from None


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, service: user_svc_dep):
    try:
        return service.update_user(
            user_id,
            email=user.email,
            username=user.username,
        )
    except NoResultFound as nrfex:
        print(nrfex)
        raise HTTPException(status_code=404, detail="User not found") from None
    except IntegrityError as ieex:
        print(ieex)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already exists",
        ) from None


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: user_svc_dep):
    try:
        service.delete_user(user_id)
    except NoResultFound as nrfex:
        print(nrfex)
        raise HTTPException(status_code=404, detail="User not found") from None
