from datetime import datetime, timezone

import pymongo
from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field

from app.models.post import Post


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(unique=True, max_length=255)


class User(UserBase, Document):
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    posts: list[Link[Post]] | None = None

    class Settings:
        name = "users"
        indexes = [
            [("created_at", pymongo.DESCENDING)],
            [("username", pymongo.TEXT), ("email", pymongo.TEXT)],
        ]


class UserRegister(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(UserBase):
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserPublic(UserBase):
    created_at: datetime


class UsersPublic(BaseModel):
    data: list[User]
