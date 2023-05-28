from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base


class BaseModelService:
    model: Base

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, **kwargs) -> Base:
        self._check_attributes_set()
        obj = self.model(**kwargs)
        self.db_session.add(obj)
        await self.db_session.commit()

        return obj

    def _check_attributes_set(self) -> None:
        assert self.model, "Attribute 'model' should be provided"
