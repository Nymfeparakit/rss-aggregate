from fastapi import FastAPI
from src.auth import router as users_routers

from src.folders.router import folders_router
from src.sources.router import sources_router

app = FastAPI()

app.include_router(users_routers.router, prefix="/auth", tags=["auth"])
app.include_router(folders_router, prefix="/folders", tags=["folders"])
app.include_router(sources_router, prefix="/sources", tags=["sources"])
