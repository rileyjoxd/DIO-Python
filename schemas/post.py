from pydantic import BaseModel

from datetime import UTC, datetime


class PostIn(BaseModel):
    title: str
    content: str
    published_at: datetime | None = None
    published: bool = False