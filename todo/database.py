from pymongo import MongoClient

from .settings import settings

client = MongoClient(f"{settings.db_url}:{settings.db_port}/")
db = client.lyteforge_db
todo_collection = db.geo_todos

todo_collection.create_index({"location": "2dsphere"})
todo_collection.create_index({"task": "text"})
