import asyncio
import json

from redis.asyncio import Redis

from app.services.broadcaster import broadcast
from app.settings import settings

CHANNEL = "events_stream"


async def redis_subscribe_loop(stop: asyncio.Event):
    backoff = 1

    while not stop.is_set():
        try:
            async with Redis.from_url(settings.redis_url) as r:
                async with r.pubsub() as pubsub:
                    await pubsub.subscribe(CHANNEL)
                    print(f"[stream_bus] subscribed to {CHANNEL}")

                    async for msg in pubsub.listen():
                        if stop.is_set():
                            break
                        if msg.get("type") != "message":
                            continue

                        raw = msg["data"]
                        try:
                            if isinstance(raw, (bytes, bytearray)):
                                raw = raw.decode("utf-8")
                            data = json.loads(raw)
                        except Exception as e:
                            print("[stream_bus] parse error:", repr(e))
                            continue

                        await broadcast.publish(data)
                        backoff = 1

        except asyncio.CancelledError:
            print("[stream_bus] cancelled")
            break
        except Exception as e:
            print("[stream_bus] error, will reconnect:", repr(e))
            await asyncio.wait_for(asyncio.sleep(backoff), timeout=None)
            backoff = min(backoff * 2, 30)

    print("[stream_bus] stop requested; exiting")
