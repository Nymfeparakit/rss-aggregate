import pytest
import pytest_asyncio
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from starlette.testclient import TestClient

import config
from src.folders.models import UserFolder
from main import app
from src.auth import current_user, User, UserCreate
from src.auth.manager import UserManager
from src.database import Base, get_async_session
from src.sources.models import Source


@pytest.fixture(scope="session")
def api_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def meta_migration():
    # setup
    sync_engine = create_engine(
        config.SYNC_DATABASE_URL + "_test"
    )
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)

    yield sync_engine

    # teardown
    Base.metadata.drop_all(sync_engine)


@pytest_asyncio.fixture
async def async_engine() -> AsyncEngine:
    # setup
    engine = create_async_engine(
        config.MAIN_DATABASE_URL + "_test"
    )

    yield engine


@pytest_asyncio.fixture
async def session(async_engine, meta_migration):
    conn = await async_engine.connect()
    trans = await conn.begin()
    session = AsyncSession(bind=conn, join_transaction_mode="create_savepoint", expire_on_commit=False)

    yield session

    await session.close()
    await trans.rollback()
    await conn.close()


@pytest_asyncio.fixture
async def user_db(session):
    yield SQLAlchemyUserDatabase(session, User)


@pytest_asyncio.fixture
async def user_test(user_db) -> User:
    user_manager = UserManager(user_db)
    user = await user_manager.create(
        UserCreate(email="test@mail.com", password="123123")
    )
    return user


@pytest_asyncio.fixture
async def override_app_client(user_test, session):
    def get_sess():
        yield session

    app.dependency_overrides[current_user] = lambda: user_test
    app.dependency_overrides[get_async_session] = get_sess

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    del app.dependency_overrides[current_user]
    del app.dependency_overrides[get_async_session]


@pytest_asyncio.fixture
async def source(session) -> Source:
    created_source = Source(name="some name", url="some url")
    session.add(created_source)
    await session.commit()

    yield created_source


@pytest_asyncio.fixture
async def folder(session, user_test) -> UserFolder:
    created_folder = UserFolder(name="some name", user=user_test)
    session.add(created_folder)
    await session.commit()

    yield created_folder
