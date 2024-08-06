from pymongo import MongoClient
from app.utils.helper import parse_json
client=MongoClient("mongodb://localhost:27017/")
db = client["course-goals"]
collection = db.users

def insert_user(data):
    data2=parse_json(data)
    insertion=collection.insert_one(data2)
    return insertion.acknowledged