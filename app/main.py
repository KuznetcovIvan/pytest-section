import redis.asyncio as redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.api import spimex_router
from app.config import settings
from app.tasks import clear_cache_task

app = FastAPI(title=settings.app_title, description=settings.description)
app.include_router(spimex_router)

redis_client = redis.from_url(settings.redis_cache_url)
scheduler = AsyncIOScheduler()


@app.on_event('startup')
async def startup():
    FastAPICache.init(
        RedisBackend(redis_client),
        prefix='spimex',
        expire=settings.expire_cache,
    )
    scheduler.add_job(
        clear_cache_task,
        CronTrigger(**settings.clear_cache_time),
        id='clear_cache',
    )
    scheduler.start()


@app.on_event('shutdown')
async def shutdown():
    scheduler.shutdown(wait=False)
    await redis_client.close()
