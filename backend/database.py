import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import settings

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
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1} to connect to MongoDB...")
                db.client = AsyncIOMotorClient(
                    settings.MONGODB_URL,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=10000,
                    socketTimeoutMS=20000
                )
                # Test the connection
                await db.client.server_info()
                db.db = db.client[settings.DATABASE_NAME]
                logger.info("✅ Successfully connected to MongoDB")
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"❌ Failed to connect to MongoDB after {max_retries} attempts")
                    raise
                logger.warning(f"⚠️ Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
    except Exception as e:
        logger.error(f"❌ Error connecting to MongoDB: {e}")
        raise

async def close_mongo_connection():
    if db.client:
        try:
            db.client.close()
            logger.info("🛑 Closed MongoDB connection")
        except Exception as e:
            logger.error(f"⚠️ Error closing MongoDB connection: {e}")
