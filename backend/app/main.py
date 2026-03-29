from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.core.router import router as core_router

app = FastAPI(
    title="Docs API",
    description="Document manager API",
    version="0.1.0",
)
app.include_router(core_router)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
