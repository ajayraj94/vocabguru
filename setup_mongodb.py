import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime

# Get URI from environment or manual input
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    MONGO_URI = "mongodb+srv://ajayraj13494_db_user:9PiUKLNslKHYbr54@cluster0.epychuv.mongodb.net/?appName=Cluster0"

DB_NAME = "mission2_bot_db"

def setup_db():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        print(f"Connecting to MongoDB...")
        # Trigger connection
        client.admin.command('ping')
        print("✅ Connection Successful!")

        # 1. Setup State Collection
        if "state" not in db.list_collection_names():
            db.create_collection("state")
            db.state.insert_one({"_id": "global_state", "last_sent_index": -1})
            print("✅ State collection initialized.")

        # 2. Setup Analytics Collection & Indexes
        if "analytics" not in db.list_collection_names():
            db.create_collection("analytics")
        
        # Create Index for Leaderboard (Descending by correct answers)
        db.analytics.create_index([("correct", DESCENDING)])
        print("✅ Analytics indexes created.")

        # 3. Setup Polls Collection & Index
        if "active_polls" not in db.list_collection_names():
            db.create_collection("active_polls")
        
        # Index for poll_id for fast lookup
        db.active_polls.create_index([("poll_id", ASCENDING)])
        # TTL Index: Automatically delete polls after 24 hours to keep DB clean
        db.active_polls.create_index("created_at", expireAfterSeconds=86400)
        print("✅ Active Polls indexes and TTL set.")

        print("\n🚀 MongoDB is now fully OPTIMIZED for Mission 2 Bot!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_db()
