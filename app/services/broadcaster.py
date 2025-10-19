import asyncio
from typing import Any


class Broadcast:
    def __init__(self):
        self._subs: set[asyncio.Queue] = set()

    async def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue[Any] = asyncio.Queue(maxsize=1000)
        self._subs.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue):
        self._subs.discard(q)

    async def publish(self, msg: Any):
        for q in list(self._subs):
            try:
                q.put_nowait(msg)
            except asyncio.QueueFull:
                pass


broadcast = Broadcast()
