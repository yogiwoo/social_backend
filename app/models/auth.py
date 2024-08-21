from pymongo import MongoClient
from app.utils.helper import parse_json
from bson import ObjectId
client=MongoClient("mongodb://localhost:27017/")
db = client["social"]
collection = db.users

def insert_user(data):
    data2=parse_json(data)
    insertion=collection.insert_one(data2)
    return insertion.acknowledged

def find_user(mobile):
    userData=collection.find_one({"$or":[{"mob":mobile}]})
    if userData:
        return userData

def find_user_byid(userId):
    userData=collection.find_one({"_id":ObjectId(userId)})
    if userData:
        return userData