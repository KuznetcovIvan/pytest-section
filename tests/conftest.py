import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db import Base, engine, get_async_session
from app.main import app

pytest_plugins = ['fixtures.data']


@pytest.fixture(scope='session')
def session_factory():
    return sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
    )


@pytest_asyncio.fixture(autouse=True)
async def override_get_async_session(session_factory):
    async def get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_async_session] = get_session
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db(trading_results, session_factory):
    assert settings.mode == 'test'
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with session_factory() as session:
        session.add_all(trading_results)
        await session.commit()
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db_session(session_factory):
    async with session_factory() as session:
        yield session
