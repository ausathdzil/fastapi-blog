from datetime import datetime, timezone

import pymongo
from beanie import Document
from pydantic import BaseModel, Field


class Post(Document):
    title: str = Field(min_length=1, max_length=50)
    published_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    summary: str = Field(min_length=1, max_length=160)
    content: str = Field(min_length=1)
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


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    summary: str = Field(min_length=1, max_length=160)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)


class PostsPublic(BaseModel):
    data: list[Post]
    count: int
    page: int
    pages: int
    size: int
    has_next: bool
    has_prev: bool


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=50)
    summary: str | None = Field(default=None, min_length=1, max_length=160)
    content: str | None = Field(default=None, min_length=1)
    author: str | None = Field(default=None, min_length=1, max_length=50)


class Message(BaseModel):
    message: str
