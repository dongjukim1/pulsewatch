import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import health, stream
from app.services import rss_client
from app.services.stream_bus import redis_subscribe_loop
from app.settings import settings
from worker.tasks import process_items

log = logging.getLogger("pulsewatch")
logging.basicConfig(level=logging.INFO)


async def poll_loop():
    while True:
        try:
            items = await rss_client.fetch_all(settings.nhk_feeds)
            process_items.delay([i.model_dump(mode="json") for i in items])
        except Exception as e:
            log.exception("poll_error: %s", e)
        await asyncio.sleep(settings.poll_interval_sec)


@asynccontextmanager
async def lifespan(app: FastAPI):
    stop = asyncio.Event()
    log.info("[lifecycle] startup")
    stream_task = asyncio.create_task(redis_subscribe_loop(stop))
    poll_task = asyncio.create_task(poll_loop())
    try:
        yield
    finally:
        log.info("[lifecycle] shutdown")
        stop.set()
        for t in (stream_task, poll_task):
            if not t.done():
                t.cancel()
        await asyncio.sleep(0)


app = FastAPI(title="PulseWatch NHK", lifespan=lifespan)
app.include_router(health.router)
app.include_router(stream.router)
