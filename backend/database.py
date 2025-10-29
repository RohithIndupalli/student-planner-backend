import asyncio
import logging
import os
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
        
        # Get MongoDB URL from environment or settings
        mongodb_url = os.getenv('MONGODB_URL') or os.getenv('MONGODB_URI') or settings.MONGODB_URL
        
        logger.info(f"🔧 Attempting to connect to MongoDB with URL: {mongodb_url.split('@')[-1]}")
        
        for attempt in range(max_retries):
            try:
                logger.info(f"🔄 Attempt {attempt + 1}/{max_retries} to connect to MongoDB...")
                
                # Create a new client with explicit parameters
                db.client = AsyncIOMotorClient(
                    mongodb_url,
                    serverSelectionTimeoutMS=10000,
                    connectTimeoutMS=10000,
                    socketTimeoutMS=30000,
                    connect=False,  # Use connect=False to handle connection manually
                    retryWrites=True,
                    w='majority',
                    appName='student-planner-backend'
                )
                
                # Force connection and get server info
                logger.info("🔍 Testing MongoDB connection...")
                await db.client.admin.command('ping')
                
                # If we get here, connection was successful
                db.db = db.client[settings.DATABASE_NAME]
                logger.info(f"✅ Successfully connected to MongoDB: {settings.DATABASE_NAME}")
                
                # Verify we can access the database
                collections = await db.db.list_collection_names()
                logger.info(f"📚 Available collections: {', '.join(collections) if collections else 'None'}")
                
                return
                
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"❌ Failed to connect to MongoDB after {max_retries} attempts")
                    logger.error(f"❌ Error details: {str(e)}")
                    raise
                    
                logger.warning(f"⚠️ Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                
    except Exception as e:
        logger.error(f"❌ Critical error connecting to MongoDB: {str(e)}")
        logger.error(f"❌ Connection was attempted with URL: {mongodb_url}")
        raise

async def close_mongo_connection():
    if db.client:
        try:
            await db.client.close()
            logger.info("🛑 Closed MongoDB connection")
        except Exception as e:
            logger.error(f"⚠️ Error closing MongoDB connection: {e}")
        finally:
            db.client = None
            db.db = None
