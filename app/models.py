from datetime import datetime
from time import timezone

import pymongo
from beanie import Document
from pydantic import Field


class Post(Document):
    title: str = Field(min_length=1, max_length=50)
    published_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    summary: str = Field(min_length=1, max_length=160)
    author: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1)

    class Settings:
        name = "posts"
        indexes = [
            [("published_at", pymongo.DESCENDING)],
            [
                ("title", pymongo.TEXT),
                ("summary", pymongo.TEXT),
            ],
        ]
