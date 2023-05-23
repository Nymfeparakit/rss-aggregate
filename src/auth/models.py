from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from src.folders.models import UserFolder

from src.database import get_async_session, Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    folders = relationship(UserFolder, backref="user")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
