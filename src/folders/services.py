from typing import List
from uuid import UUID

import aiohttp
import feedparser
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.auth import User
from src.database import get_async_session
from src.exceptions import NotFoundHTTPException
from src.folders import schemas, models
from src.rss.exceptions import InvalidRSSURL
from src.rss.parsers import RSSFeedParser, RSSElementsParser
from src.sources.models import Source
from src.sources.schemas import SourceCreate


class UserFolderService:
    # todo: add typehint
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.url_parser = RSSFeedParser()

    async def create(
        self, folder: schemas.UserFolderCreate, user: User
    ) -> models.UserFolder:
        db_folder = models.UserFolder(**folder.dict(), user_id=user.id)
        self.db_session.add(db_folder)
        await self.db_session.commit()

        return db_folder

    async def list(self, user: User) -> List[models.UserFolder]:
        stmt = select(models.UserFolder).where(models.UserFolder.user_id == user.id)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    # todo: move common code to some base service?
    async def retrieve(self, folder_id: UUID, user: User) -> models.UserFolder:
        return await self.find(folder_id, user)

    async def update(self, folder_id: UUID, user: User, folder: schemas.UserFolderUpdate) -> models.UserFolder:
        instance = await self.find(folder_id, user)

        data_to_update = folder.dict()
        for k, v in data_to_update.items():
            setattr(instance, k, v)
        await self.db_session.commit()

        return instance

    async def delete(self, folder_id: UUID, user: User) -> None:
        instance = await self.find(folder_id, user)

        await self.db_session.delete(instance)
        await self.db_session.commit()

    async def find(self, folder_id: UUID, user: User) -> models.UserFolder:
        stmt = select(models.UserFolder).where(
            models.UserFolder.id == folder_id,
            models.UserFolder.user_id == user.id,
        ).options(selectinload(models.UserFolder.sources))
        result = await self.db_session.execute(stmt)
        instance = result.scalars().first()
        if instance is None:
            raise NotFoundHTTPException
        return instance

    async def create_folder_source(self, folder_id: UUID, user: User, source_schema_obj: SourceCreate):
        try:
            folder = await self.find(folder_id, user)

            # check if passed url is valid
            parsed_data = await self.url_parser.try_parse_rss(source_schema_obj.url)

            # todo: upload rss icon if it has link to it
            file_name = await RSSElementsParser().save_feed_image(parsed_data)
            source_data = dict(**source_schema_obj.dict(), folder_id=folder.id)
            if file_name:
                source_data.update(icon=file_name)
            source_obj = Source(**source_data)

            self.db_session.add(source_obj)
            await self.db_session.commit()

            return source_obj
        except InvalidRSSURL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Passed url does not contain valid rss data"
            )


def get_folders_service(db_session=Depends(get_async_session)):
    return UserFolderService(db_session=db_session)
