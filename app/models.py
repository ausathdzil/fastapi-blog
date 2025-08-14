from datetime import datetime
from time import timezone

from beanie import Document
from pydantic import Field

class Post(Document):
    title: str = Field(min_length=1, max_length=50)
    published_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    summary: str = Field(min_length=1, max_length=160)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)

    class Settings:
        name = "posts"
