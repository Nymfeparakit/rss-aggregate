from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from src.auth import current_user, User
from src.folders import schemas
from src.folders.schemas import UserFolderCreate, UserFolderUpdate
from src.folders.services import (
    get_folders_service, UserFolderService,
)
from src.sources.schemas import SourceCreate, Source

folders_router = APIRouter()


@folders_router.post("", response_model=schemas.UserFolder, status_code=status.HTTP_201_CREATED)
async def create_folder(
    folder_create: UserFolderCreate,
    folders_service: UserFolderService = Depends(get_folders_service),
    user: User = Depends(current_user),
):
    return await folders_service.create(folder_create, user)


@folders_router.get("", response_model=List[schemas.UserFolder])
async def list_folders(
    folders_service: UserFolderService = Depends(get_folders_service),
    user: User = Depends(current_user),
):
    return await folders_service.list(user)


@folders_router.get("/{folder_id}", response_model=schemas.UserFolder)
async def retrieve_folder(
    folder_id: UUID,
    user: User = Depends(current_user),
    folders_service: UserFolderService = Depends(get_folders_service),
):
    folder = await folders_service.retrieve(folder_id, user)
    return folder


@folders_router.put("/{folder_id}", response_model=schemas.UserFolder)
async def update_folder(
    folder_id: UUID,
    folder_create: UserFolderUpdate,
    user: User = Depends(current_user),
    folders_service: UserFolderService = Depends(get_folders_service),
):
    folder = await folders_service.update(folder_id, user, folder_create)
    return folder


@folders_router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(
    folder_id: UUID,
    user: User = Depends(current_user),
    folders_service: UserFolderService = Depends(get_folders_service),
):
    await folders_service.delete(folder_id, user)


@folders_router.post("/{folder_id}/sources", response_model=Source)
async def create_folder_source(
        folder_id: UUID,
        source: SourceCreate,
        user: User = Depends(current_user),
        folders_service: UserFolderService = Depends(get_folders_service),
):
    return await folders_service.create_folder_source(folder_id, user, source)
