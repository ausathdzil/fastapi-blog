from datetime import datetime, timezone

import pymongo
from beanie import Document
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    summary: str = Field(min_length=1, max_length=160)
    content: str = Field(min_length=1)


class Post(PostBase, Document):
    published_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    author: str = Field(min_length=1, max_length=50)

    class Settings:
        name = "posts"
        indexes = [
            [("published_at", pymongo.DESCENDING)],
            [
                ("title", pymongo.TEXT),
                ("summary", pymongo.TEXT),
            ],
        ]


class PostCreate(PostBase):
    author: str = Field(min_length=1, max_length=50)


class PostsPublic(BaseModel):
    data: list[Post]
    count: int
    page: int
    pages: int
    size: int
    has_next: bool
    has_prev: bool


class PostUpdate(PostBase):
    pass


class Message(BaseModel):
    message: str
