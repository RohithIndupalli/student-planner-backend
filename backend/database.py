from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None
    
db = Database()

async def get_database():
    if db.db is None:
        await connect_to_mongo()
    return db.db

async def connect_to_mongo():
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
        # Test the connection
        await db.client.server_info()
        db.db = db.client[settings.DATABASE_NAME]
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise

async def close_mongo_connection():
    if db.client:
        db.client.close()
        logger.info("Closed MongoDB connection")
