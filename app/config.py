from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'SPIMEX API'
    description: str = 'Cервис для получения данных по итогам торгов'
    max_days_range: int = 7
    max_days_limit: int = 365
    expire_cache: int = 60 * 60 * 24
    clear_cache_time: dict = {'hour': 14, 'minute': 11}
    database_url: str
    redis_cache_url: str

    class Config:
        env_file = '.env'


settings = Settings()
