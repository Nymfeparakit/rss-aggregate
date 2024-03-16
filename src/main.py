from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as users_router
from src.feeds.router import feeds_router
from src.folders.router import folders_router
from src.sources.router import sources_router

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/auth", tags=["auth"])
app.include_router(folders_router, prefix="/folders", tags=["folders"])
app.include_router(sources_router, prefix="/sources", tags=["sources"])
app.include_router(feeds_router, prefix="/feeds", tags=["feeds"])
