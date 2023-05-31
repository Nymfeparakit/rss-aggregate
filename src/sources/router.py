from fastapi import APIRouter, Depends
from starlette import status

from src.auth import User, current_user
from src.sources import schemas
from src.sources.services import SourceService, get_sources_service

sources_router = APIRouter()


@sources_router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Source)
async def create_source(
    source: schemas.SourceCreate,
    user: User = Depends(current_user),
    sources_service: SourceService = Depends(get_sources_service),
):
    return await sources_service.create(source=source)


@sources_router.post("/folder-items", status_code=status.HTTP_201_CREATED, response_model=schemas.FolderItem)
async def create_folder_item(
    folder_item: schemas.FolderItem,
    user: User = Depends(current_user),
    sources_service: SourceService = Depends(get_sources_service),
):
    return await sources_service.create_folder_item(folder_item, user)
