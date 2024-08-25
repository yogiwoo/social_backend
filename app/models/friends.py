from pymongo import MongoClient
from app.utils.helper import parse_json
from bson import ObjectId
client=MongoClient("mongodb://localhost:27017/")
db = client["social"]
collection = db.pending_friends
def create_friends_list(data):
    data2=parse_json(data)
    insert=collection.insert_one(data2)
    return insert.acknowledged


def find_friends_list(uid):
    data2=collection.find_one({"userId.$oid":uid})
    if data2:
        return data2
    else:
        return {}

def update_friend_list_pending(data,userId):
    data2=parse_json(data)
    updatelist=collection.update_one({"userId.$oid":userId},{"$push":{"friendList":data2}})
    if updatelist:
        return updatelist.acknowledged

#====================================================friend list(collection 2)=====================================================================
collection2=db.friends
def find_friends_list_data(uid):
    data2=collection2.find_one({"userId":ObjectId(uid)})
    if data2:
        return data2

def create_friends_list_data(data):
    data2=parse_json(data)
    insert=collection2.insert_one(data2)
    return insert.acknowledged

def update_friend_list_data(data,userId):
    data2=parse_json(data)
    updatelist=collection2.update_one({"userId.$oid":userId},{"$push":{"friendList":data2}})
    if updatelist:
        return updatelist.acknowledged 

def pop_pending_req(uuid,userId):
    remove=collection.update_one({"userId.$oid":uuid},{'$pull': {'pendingList': {'userId.$oid':userId}}})
    if remove:
        return remove.acknowledged