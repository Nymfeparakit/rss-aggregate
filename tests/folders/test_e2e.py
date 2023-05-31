import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.folders.models import UserFolder


@pytest.mark.asyncio
async def test_create_folder(override_app_client: AsyncClient, session: AsyncSession):
    input_data = {"name": "test name"}

    response = await override_app_client.post("http://test/folders", json=input_data)

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert "id" in response_data
    stmt = select(UserFolder).where(UserFolder.id == response_data["id"])
    result = await session.execute(stmt)
    folder = result.scalar_one()
    assert folder.name == input_data["name"]
