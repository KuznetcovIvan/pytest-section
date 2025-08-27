import pytest_asyncio
from fakeredis.aioredis import FakeRedis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db import Base

pytest_plugins = ['fixtures.data']

engine = create_async_engine(settings.database_url)

TestingSessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db(trading_results):
    assert settings.mode == 'test'
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        session.add_all(trading_results)
        await session.commit()
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


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
