from pymongo import MongoClient

client=MongoClient("mongodb://localhost:27017/")
db = client["course-goals"]
collection = db.goals

def get_all_items():
    return list(collection.find({},{'_id':False}))

def add_item(text):
    collection.insert_one({'text': text})