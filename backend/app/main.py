from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.users import router as users_router
from app.middleware.auth import AuthMiddleware

app = FastAPI(
    title="Docs API",
    description="Document manager API",
    version="0.1.0",
)
app.include_router(health_router)
app.include_router(users_router)
app.add_middleware(AuthMiddleware)
