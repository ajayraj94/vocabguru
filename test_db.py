from pymongo import MongoClient
import sys
import time

uri = "mongodb+srv://ajayraj13494_db_user:9PiUKLNslKHYbr54@cluster0.epychuv.mongodb.net/?appName=Cluster0"
print("Attempting to connect to MongoDB Atlas...")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)
