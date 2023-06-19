from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.config import global_settings

engine = create_async_engine(global_settings.main_db_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
