import pytest_asyncio
from fakeredis.aioredis import FakeRedis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db import Base
from app.main import app

pytest_plugins = ['fixtures.data']

engine = create_async_engine(settings.database_url)

TestingSessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db():
    assert settings.mode == 'test'
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def load_trading_results(setup_db, trading_results):
    async with TestingSessionLocal() as session:
        session.add_all(trading_results)
        await session.commit()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def init_cache():
    redis = FakeRedis()
    FastAPICache.init(RedisBackend(redis), prefix='test')
    yield
    await redis.flushall()
    await redis.aclose()


@pytest_asyncio.fixture()
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope='session')
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client
