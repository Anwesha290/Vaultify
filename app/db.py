from pymongo import MongoClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize MongoDB client
try:
    client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.server_info()
    logger.info("Successfully connected to MongoDB")
    db = client["vaultify"]
    collection = db["secrets"]
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise
