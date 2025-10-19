import json
import os

import redis

from app.services.tokenizer import extract_terms
from worker.celery_app import celery


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"{name} environment variable is required")
    return value


REDIS_URL = require_env("REDIS_URL")
rpub = redis.Redis.from_url(REDIS_URL)


@celery.task(name="worker.tasks.process_items")
def process_items(items: list[dict]):
    enriched = []
    for it in items:
        text = (it.get("title") or "") + "\n" + (it.get("description") or "")
        it["tokens"] = extract_terms(text)
        enriched.append(it)

    payload = {
        "type": "batch",
        "count": len(enriched),
        "samples": enriched[:3],
    }
    rpub.publish("events_stream", json.dumps(payload, ensure_ascii=False))
    return {"ok": True, "count": len(enriched)}
