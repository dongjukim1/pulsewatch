import os

from celery import Celery


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"{name} environment variable is required")
    return value


redis_url = require_env("REDIS_URL")
celery = Celery(
    "pulsewatch",
    broker=redis_url,
    backend=redis_url,
)
celery.conf.task_routes = {
    "worker.tasks.process_items": {"queue": "events"},
}

import worker.tasks
