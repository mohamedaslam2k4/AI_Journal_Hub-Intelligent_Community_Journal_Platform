from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import get_settings

client: AsyncIOMotorClient | None = None

def get_database() -> AsyncIOMotorDatabase:
    if client is None:
        raise RuntimeError("MongoDB client is not initialized")
    return client[get_settings().mongodb_db]

async def connect_to_mongo() -> None:
    global client
    client = AsyncIOMotorClient(get_settings().mongodb_uri)
    db = get_database()
    await db.users.create_index("email", unique=True)
    await db.journals.create_index([("visibility", 1), ("moderation_status", 1), ("created_at", -1)])
    await db.journals.create_index([("author_id", 1), ("updated_at", -1)])
    await db.ai_analysis.create_index("journal_id", unique=True)

async def close_mongo() -> None:
    if client:
        client.close()
