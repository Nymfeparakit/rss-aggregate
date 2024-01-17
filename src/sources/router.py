from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.auth import User, current_user
from src.sources import schemas
from src.sources.services import SourceService, get_sources_service

sources_router = APIRouter()


@sources_router.get("", response_model=List[schemas.Source])
async def list_sources(
    user: User = Depends(current_user),
    sources_service: SourceService = Depends(get_sources_service),
):
    return await sources_service.find_sources_by_user(user)
