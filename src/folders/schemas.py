from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserFolderBase(BaseModel):
    name: Optional[str]


class UserFolderCreate(UserFolderBase):
    pass


class UserFolder(UserFolderBase):
    # todo: how to show id as first field? (how to change order)
    id: Optional[UUID]

    class Config:
        orm_mode = True
