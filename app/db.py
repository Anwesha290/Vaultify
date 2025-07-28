from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Get the full connection string from environment variables
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    # Fallback to individual components if MONGO_URI is not set
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    cluster = os.getenv("MONGO_CLUSTER")
    
    if all([username, password, cluster]):
        MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"
    else:
        raise ValueError("MongoDB connection not properly configured. Please set MONGO_URI or all of MONGO_USERNAME, MONGO_PASSWORD, and MONGO_CLUSTER")

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.server_info()
    db = client["vaultify"]
    collection = db["secrets"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise
