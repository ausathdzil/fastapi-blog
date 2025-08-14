from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.core.config import settings
from app.models import Post


async def init_db():
    client = AsyncMongoClient(settings.MONGO_CONNECTION_STRING)
    await init_beanie(
        database=client[settings.MONGO_DB],
        document_models=[Post],
    )
