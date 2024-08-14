from pymongo import MongoClient
from app.utils.helper import parse_json
client=MongoClient("mongodb://localhost:27017/")
db = client["social"]
collection = db.users

def insertPost(data):
    data2=parse_json(data)
    
    return true