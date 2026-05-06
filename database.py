import os
from pymongo import MongoClient
from datetime import datetime

# Load configuration from environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "mission2_bot_db")

# Initialize MongoDB Client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
state_col = db["state"]
analytics_col = db["analytics"]
polls_col = db["active_polls"]

def get_state():
    """Gets the last sent index from DB."""
    state = state_col.find_one({"_id": "global_state"})
    if not state:
        return {"last_sent_index": -1}
    return state

def save_state(index):
    """Saves the last sent index to DB."""
    state_col.update_one(
        {"_id": "global_state"},
        {"$set": {"last_sent_index": index}},
        upsert=True
    )

def update_analytics(user_id, name, is_correct):
    """Updates lifetime and session-like analytics in MongoDB."""
    user_id = str(user_id)
    
    # Update or insert user record
    update_query = {
        "$set": {"name": name, "last_active": datetime.utcnow()},
        "$inc": {"total": 1}
    }
    if is_correct:
        update_query["$inc"]["correct"] = 1
    
    analytics_col.update_one({"_id": user_id}, update_query, upsert=True)

def get_leaderboard(limit=10):
    """Retrieves top performers."""
    users = list(analytics_col.find().sort("correct", -1).limit(limit))
    return users

def add_active_poll(poll_id, correct_index, chat_id):
    """Tracks an open poll."""
    polls_col.insert_one({
        "poll_id": poll_id,
        "correct_index": correct_index,
        "chat_id": chat_id,
        "created_at": datetime.utcnow()
    })

def get_poll_data(poll_id):
    """Retrieves data for a specific poll."""
    return polls_col.find_one({"poll_id": poll_id})

def clear_active_polls():
    """Clears tracked polls (e.g., at session end)."""
    polls_col.delete_many({})
