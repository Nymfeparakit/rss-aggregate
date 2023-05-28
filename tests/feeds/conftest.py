import pytest_asyncio

from src.folders.models import UserFolder, FolderHasSourceAssociation
from src.sources.models import Source


@pytest_asyncio.fixture
async def sources(session, user_test):
    # todo: don't user real urls
    folder = UserFolder(user=user_test, name="some folder")
    session.add(folder)
    await session.commit()
    urls = ["https://vc.ru/rss/new", "https://realpython.com/atom.xml"]
    sources = [Source(url=url, name=f"name{idx}") for idx, url in enumerate(urls)]
    for source in sources:
        session.add(source)
        await session.commit()
        folder_item = FolderHasSourceAssociation(source=source, folder=folder)
        session.add(folder_item)
        await session.commit()
    yield sources
