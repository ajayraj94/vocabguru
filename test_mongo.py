from pymongo import MongoClient

# Testing with the password from the screenshot (small 'l')
uri = "mongodb+srv://ajayraj13494_db_user:9PiUKLNslKHYbr54@cluster0.epychuv.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ MongoDB Connection Successful with small 'l'!")
except Exception as e:
    print(f"❌ Connection failed with small 'l': {e}")

# Testing with Capital 'I' just in case
uri_i = "mongodb+srv://ajayraj13494_db_user:9PiUKLNsIKHYbr54@cluster0.epychuv.mongodb.net/?appName=Cluster0"
try:
    client = MongoClient(uri_i, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ MongoDB Connection Successful with Capital 'I'!")
except Exception as e:
    print(f"❌ Connection failed with Capital 'I': {e}")
