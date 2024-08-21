from pymongo import MongoClient
from app.utils.helper import parse_json
from bson import ObjectId
client=MongoClient("mongodb://localhost:27017/")
db = client["social"]
collection = db.posts


def insertPost(data):

    data2=parse_json(data)
    insert=collection.insert_one(data2)
    return insert.acknowledged

def updateData(data,pid):
    data2=parse_json(data)
    update=collection.update_one({"_id":ObjectId(pid)},{'$set':data2})
    return update.acknowledged

def delete(pid):
    delete=collection.delete_one({"_id":ObjectId(pid)})
    print("***************************************************",delete)
    return delete.acknowledged

def hide(pid):
    hide=collection.update_one({"_id":ObjectId(pid)},{"$set":{"isHidden":True}})
    return hide.acknowledged