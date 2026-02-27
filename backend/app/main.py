from fastapi import FastAPI

from app.core.router import router as core_router

app = FastAPI(
    title="Docs API",
    description="Document manager API",
    version="0.1.0",
)
app.include_router(core_router)
