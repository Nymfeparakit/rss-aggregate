from uuid import UUID

from pydantic import BaseModel, HttpUrl


class SourceBase(BaseModel):
    name: str
    url: HttpUrl  # todo: we should also check that it's a valid rss?


class SourceCreate(SourceBase):
    pass


class Source(SourceBase):
    class Config:
        orm_mode = True


class FolderItem(BaseModel):
    source_id: UUID
    folder_id: UUID

    class Config:
        orm_mode = True
