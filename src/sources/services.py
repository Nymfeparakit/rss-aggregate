from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import User
from src.database import get_async_session
from src.folders.models import UserFolder
from src.folders.services import UserFolderService, get_folders_service
from src.service import BaseModelService
from src.sources import models


class SourceService(BaseModelService):
    model = models.Source

    def __init__(self, db_session: AsyncSession, folder_service: UserFolderService):
        self.folder_service = folder_service
        super().__init__(db_session)

    async def find_sources_by_user(self, user: User):
        stmt = select(models.Source.id, models.Source.name, models.Source.url).join(UserFolder).where(UserFolder.user_id == user.id)
        results = await self.db_session.execute(stmt)
        return results.all()


def get_sources_service(db_session=Depends(get_async_session)) -> SourceService:
    folder_service = get_folders_service(db_session)
    return SourceService(db_session=db_session, folder_service=folder_service)
