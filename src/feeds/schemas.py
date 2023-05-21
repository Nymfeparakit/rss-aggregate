from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class SourceBase(BaseModel):
    name: Optional[str]
    url: HttpUrl  # todo: we should also check that it's a valid rss


class SourceCreate(SourceBase):
    pass


class Source(SourceBase):
    folder_id: UUID

    class Config:
        orm_mode = True


class SourceFolderBase(BaseModel):
    name: Optional[str]


class SourceFolderCreate(SourceFolderBase):
    pass


class SourceFolder(SourceFolderBase):
    # todo: how to show id as first field? (how to change order)
    id: Optional[UUID]

    class Config:
        orm_mode = True
