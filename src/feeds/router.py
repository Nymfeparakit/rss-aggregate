from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from src.auth import current_user, User
from src.feeds import schemas
from src.feeds.schemas import SourceFolderCreate
from src.feeds.services import get_folders_service, SourceFolderService

folders_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@folders_router.post("", response_model=schemas.SourceFolder)
async def create_folder(
    folder_create: SourceFolderCreate,
    folders_service: SourceFolderService = Depends(get_folders_service),
    user: User = Depends(current_user),
):
    return await folders_service.create(folder_create, user)


@folders_router.get("", response_model=List[schemas.SourceFolder])
async def list_folders(
    folders_service: SourceFolderService = Depends(get_folders_service),
    user: User = Depends(current_user),
):
    return await folders_service.list(user)


@folders_router.get("/{folder_id}", response_model=schemas.SourceFolder)
async def retrieve_folder(
    folder_id: UUID,
    user: User = Depends(current_user),
    folders_service: SourceFolderService = Depends(get_folders_service),
):
    folder = await folders_service.retrieve(folder_id, user)
    return folder


@folders_router.put("/{folder_id}", response_model=schemas.SourceFolder)
async def update_folder(
    folder_id: UUID,
    folder_create: SourceFolderCreate,
    user: User = Depends(current_user),
    folders_service: SourceFolderService = Depends(get_folders_service),
):
    folder = await folders_service.update(folder_id, user, folder_create)
    return folder


@folders_router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(
    folder_id: UUID,
    user: User = Depends(current_user),
    folders_service: SourceFolderService = Depends(get_folders_service)
):
    await folders_service.delete(folder_id, user)
