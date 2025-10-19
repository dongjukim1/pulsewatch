import os

from pydantic import BaseModel


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"{name} environment variable is required")
    return value


class Settings(BaseModel):
    app_env: str = require_env("APP_ENV")
    poll_interval_sec: int = int(require_env("POLL_INTERVAL_SEC"))
    nhk_feeds: list[str] = require_env("NHK_FEEDS").split(",")
    redis_url: str = require_env("REDIS_URL")


settings = Settings()
