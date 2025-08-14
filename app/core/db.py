from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.core.config import settings
from app.models import Post


async def init():
    uri = settings.MONGO_CONNECTION_STRING
    client = AsyncMongoClient(uri)
    db = client[settings.MONGO_DB]
    await init_beanie(
        database=db,
        document_models=[Post],
    )
