import asyncio
from datetime import datetime, timezone

import aiohttp
import feedparser

from app.models import NewsItem


async def fetch_feed(session: aiohttp.ClientSession, url: str) -> list[NewsItem]:
    async with session.get(url, timeout=10) as resp:
        text = await resp.text()
    feed = feedparser.parse(text)
    out: list[NewsItem] = []
    for e in feed.entries:
        title = e.get("title", "").strip()
        desc = e.get("summary", "").strip()
        link = e.get("link", "")
        published = None
        if hasattr(e, "published_parsed") and e.published_parsed:
            published = datetime(*e.published_parsed[:6], tzinfo=timezone.utc)
        else:
            published = datetime.now(timezone.utc)
        out.append(
            NewsItem(
                feed=url,
                title=title,
                description=desc,
                url=link,
                published_at=published,
            )
        )
    return out


async def fetch_all(feeds: list[str]) -> list[NewsItem]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_feed(session, u) for u in feeds]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        items: list[NewsItem] = [x for sub in results for x in sub]
        return items
