from pymongo import MongoClient

uri = "mongodb+srv://ajayraj13494_db_user:9PiUKLNslKHYbr54@cluster0.epychuv.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["mission2_db"]
state_col = db["state"]

# Set last_sent_index to 95 (so next quiz starts at 96, which is the 97th word)
result = state_col.update_one(
    {"_id": "bot_state"},
    {"$set": {"last_sent_index": 95}},
    upsert=True
)

print(f"✅ Updated last_sent_index to 95. Modified: {result.modified_count}")
