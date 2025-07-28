from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from app.config import settings
import logging
import os

logger = logging.getLogger(__name__)

try:
    # Get MongoDB URI from settings (which now handles the required check)
    mongodb_uri = settings.MONGODB_URI
    
    logger.info(f"Connecting to MongoDB...")
    
    # Initialize client with connection pooling and timeouts
    client = MongoClient(
        mongodb_uri,
        serverSelectionTimeoutMS=5000,  # 5 second timeout
        socketTimeoutMS=30000,          # 30 second socket timeout
        connectTimeoutMS=10000,         # 10 second connection timeout
        maxPoolSize=100,                # Maximum number of connections
        retryWrites=True,
        w='majority'
    )
    
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
    
    # Get database and collection
    db = client["vaultify"] # Gets database from connection string
    collection = db["secrets"]
    
except ConfigurationError as e:
    logger.error(f"MongoDB configuration error: {e}")
    raise
    
except ConnectionFailure as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    logger.error(f"Connection string: {mongodb_uri[:50]}...")
    raise
    
except Exception as e:
    logger.error(f"Unexpected error connecting to MongoDB: {e}")
    raise
