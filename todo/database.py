from pymongo import MongoClient

client = MongoClient(f"mongodb://127.0.0.1:27017/")
db = client.lyteforge_db
todo_collection = db.geo_todos

todo_collection.create_index({"location": "2dsphere"})
todo_collection.create_index({"task": "text"})
