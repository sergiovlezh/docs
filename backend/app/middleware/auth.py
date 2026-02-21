from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import SessionLocal
from app.services.auth_service import AuthService

PUBLIC_PATHS = {
    "/health",
    "/auth/login",
    "/auth/register",
}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()

        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing token"},
            )

        with SessionLocal() as session:
            try:
                user = AuthService(session).get_user_by_token(token)
                request.state.user = user
            except NoResultFound:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid or expired token"},
                )

        return await call_next(request)
