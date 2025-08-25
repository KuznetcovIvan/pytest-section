from fastapi_cache import FastAPICache


async def clear_cache_task():
    await FastAPICache.clear()
