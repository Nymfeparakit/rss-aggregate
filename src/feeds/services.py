from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select

from src.auth import User
from src.database import get_async_session
from src.exceptions import NotFoundHTTPException
from src.feeds import schemas, models


class SourceFolderService:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create(
        self, folder: schemas.SourceFolderCreate, user: User
    ) -> models.SourcesFolder:
        db_folder = models.SourcesFolder(**folder.dict(), user_id=user.id)
        self.db_session.add(db_folder)
        await self.db_session.commit()

        return db_folder

    # todo: type hint for return type?
    async def list(self, user: User):
        stmt = select(models.SourcesFolder).where(models.SourcesFolder.user_id == user.id)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    # todo: move common code to some base service?
    async def retrieve(self, folder_id: UUID, user: User) -> models.SourcesFolder:
        return await self._find_instance(folder_id, user)

    async def update(self, folder_id: UUID, user: User, folder: schemas.SourceFolderCreate):
        instance = await self._find_instance(folder_id, user)

        data_to_update = folder.dict()
        for k, v in data_to_update.items():
            setattr(instance, k, v)
        await self.db_session.commit()

        return instance

    async def delete(self, folder_id: UUID, user: User):
        instance = await self._find_instance(folder_id, user)

        await self.db_session.delete(instance)
        await self.db_session.commit()

    async def _find_instance(self, folder_id: UUID, user: User) -> models.SourcesFolder:
        stmt = select(models.SourcesFolder).where(
            models.SourcesFolder.id == folder_id,
            models.SourcesFolder.user_id == user.id,
        )
        result = await self.db_session.execute(stmt)
        instance = result.scalars().first()
        if instance is None:
            raise NotFoundHTTPException
        return instance


async def get_folders_service(db_storage=Depends(get_async_session)):
    return SourceFolderService(db_session=db_storage)
