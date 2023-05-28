from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import User
from src.database import get_async_session
from src.folders.models import FolderHasSourceAssociation, UserFolder
from src.folders.services import UserFolderService, get_folders_service
from src.service import BaseModelService
from src.sources import schemas, models


class SourceService(BaseModelService):
    model = models.Source

    def __init__(self, db_session: AsyncSession, folder_service: UserFolderService):
        self.folder_service = folder_service
        super().__init__(db_session)

    async def create(self, source: schemas.SourceCreate) -> models.Source:
        return await super().create(**source.dict())

    async def create_folder_item(self, item: schemas.FolderItem, user: User) -> FolderHasSourceAssociation:
        # todo: how to do less queries?
        folder = await self.folder_service.find(item.folder_id, user)
        result = await self.db_session.execute(select(models.Source).where(models.Source.id == item.source_id))
        source = result.scalars().first()
        folder_item = FolderHasSourceAssociation(source=source)
        folder.sources.append(folder_item)
        await self.db_session.commit()

        return folder_item

    async def find_sources_by_user(self, user: User):
        stmt = select(models.Source.name, models.Source.url).join(FolderHasSourceAssociation).join(UserFolder).where(UserFolder.user_id == user.id)
        return await self.db_session.execute(stmt)


def get_sources_service(db_session=Depends(get_async_session)) -> SourceService:
    folder_service = get_folders_service(db_session)
    return SourceService(db_session=db_session, folder_service=folder_service)
