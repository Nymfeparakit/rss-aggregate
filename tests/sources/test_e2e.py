import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.folders.models import UserFolder, FolderHasSourceAssociation
from src.sources.models import Source


@pytest.mark.asyncio
async def test_create_source(override_app_client: AsyncClient, session: AsyncSession):
    input_data = {"name": "test name", "url": "http://example.com"}

    response = await override_app_client.post("http://test/sources", json=input_data)

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert "id" in response_data
    stmt = select(Source).where(Source.id == response_data["id"])
    result = await session.execute(stmt)
    source = result.scalar_one()
    assert source.name == input_data["name"]
    assert source.url == input_data["url"]


@pytest.mark.asyncio
async def test_create_folder_item(
    override_app_client: AsyncClient,
    session: AsyncSession,
    source: Source,
    folder: UserFolder,
):
    folder_id_str = str(folder.id)
    source_id_str = str(source.id)
    input_data = {"source_id": source_id_str, "folder_id": folder_id_str}

    response = await override_app_client.post(
        "http://test/sources/folder-items", json=input_data
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert "folder_id" in response_data
    assert "source_id" in response_data
    stmt = select(FolderHasSourceAssociation).where(
        FolderHasSourceAssociation.folder_id == folder.id,
        FolderHasSourceAssociation.source_id == source.id,
    )
    result = await session.execute(stmt)
    result.scalar_one()
