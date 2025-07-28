import ssl
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

def test_connection():
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Get MongoDB URI from environment variables
        mongodb_uri = os.getenv("MONGODB_URI")
        
        if not mongodb_uri:
            raise ValueError("MONGODB_URI not found in .env file")
            
        print(f"🔍 Testing connection to MongoDB...")
        print(f"   URI: {mongodb_uri.split('@')[-1].split('?')[0]}...")  # Show only cluster info, not credentials
        
        client = MongoClient(
            mongodb_uri,
            serverSelectionTimeoutMS=5000,
            tls=True,
            tlsAllowInvalidCertificates=False,
            server_api=ServerApi('1')
        )
        
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB")
        
        # Test database access
        db = client.get_database()
        print(f"✅ Successfully accessed database: {db.name}")
        
        # Test collection access
        collection = db["secrets"]
        print(f"✅ Successfully accessed collection: {collection.name}")
        
    except Exception as e:
        print(f"\n❌ Connection failed:")
        print(f"   Error: {str(e)}\n")
        print("Troubleshooting tips:")
        print("1. Check if MONGODB_URI is correctly set in your .env file")
        print("2. Verify your IP is whitelisted in MongoDB Atlas")
        print("3. Check if your MongoDB Atlas cluster is running")
        print("4. Try adding `tlsAllowInvalidCertificates=true` to your connection string")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    test_connection()