from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class NewsItem(BaseModel):
    source: str = "nhk"
    feed: str
    title: str
    description: Optional[str] = None
    url: str
    published_at: datetime
    tokens: List[str] = []
