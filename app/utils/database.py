from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["notes_app"]
# users_collection = db["users"]
# notes_collection = db["notes"]
try:
    client = MongoClient("mongodb://127.0.0.1:27017/")
    print("Connected to MongoDB!")
    db = client["notes_app"]
    users_collection = db["users"]
    notes_collection = db["notes"]
except Exception as e:
    print(f"Error: {e}")