from fastapi import FastAPI
from src.auth import router as users_routers

from src.feeds.router import folders_router

app = FastAPI()

app.include_router(users_routers.router, prefix="/auth", tags=["auth"])
app.include_router(folders_router, prefix="/folders", tags=["folders"])
