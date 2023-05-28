import pytest
import pytest_asyncio
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from httpx import AsyncClient
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from starlette.testclient import TestClient

import config
from main import app
from src.auth import current_user, User, UserCreate
from src.auth.manager import UserManager
from src.database import Base, get_async_session
from src.sources.models import Source


@pytest.fixture(scope="session")
def api_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
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


# async def get_test_session():
#     test_engine = create_async_engine(
#         config.MAIN_DATABASE_URL+ '_test',
#         echo=False,
#     )
#
#     # expire_on_commit=False will prevent attributes from being expired
#     # after commit.
#     async_sess = sessionmaker(
#         test_engine, expire_on_commit=False, class_=AsyncSession
#     )
#     async with async_sess() as sess, sess.begin():
#         yield sess


@pytest_asyncio.fixture
async def session(async_engine):
    conn = await async_engine.connect()
    trans = await conn.begin()
    session = AsyncSession(bind=conn, join_transaction_mode="create_savepoint", expire_on_commit=False)

    yield session

    await session.close()
    await trans.rollback()
    await conn.close()


@pytest_asyncio.fixture
async def source(session):
    source = Source(name="some name", url="some url")
    session.add(source)
    await session.commit()

    yield source


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


# @pytest_asyncio.fixture
# async def session2(session):
#     async with async_session() as sess, sess.begin():
#         yield sess


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
