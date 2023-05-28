from pydantic import BaseModel, HttpUrl


class Article(BaseModel):
    title: str
    summary: str
    link: HttpUrl
