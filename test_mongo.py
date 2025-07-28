from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Your MongoDB URI
uri = "mongodb+srv://Anwesha_Guha:PedroIsaac_76@vaultify-vault.yxcvdsv.mongodb.net/?retryWrites=true&w=majority&tls=true"

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)  # 5 seconds timeout
    client.server_info()  # Trigger connection
    print("✅ Successfully connected to MongoDB Atlas!")
except ConnectionFailure as e:
    print("❌ Could not connect to MongoDB Atlas:")
    print(e)
