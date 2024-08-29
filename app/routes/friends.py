from flask import Blueprint,jsonify,request
from datetime import datetime
from app.utils.mongo import collection
from app.models.friends import find_friends_list,create_friends_list,update_friend_list_pending,update_friend_list_data,find_friends_list_data,create_friends_list_data,pop_pending_req,getFriendsList
from flask_jwt_extended import get_jwt_identity,get_jwt,jwt_required
friend_bp=Blueprint('friend',__name__)
from app.utils.helper import parse_json,serialize_doc,convertObjectid
from bson import ObjectId
from app.models.auth import find_user,find_user_byid

@friend_bp.route("/addFriend",methods=["POST"])
@jwt_required()
def addFriend():
    #Send friend request
    data=request.get_json()
    claims = get_jwt() 
    friend_list=find_friends_list(claims["id"])
    xx={
        "name":data["name"],
        "userId":ObjectId(data["userId"]),
        "image":data["image"],
        "time":data["addedAt"],
        "incoming":False
    }
    if friend_list:
        updation=update_friend_list_pending(xx,claims["id"])
        if updation==True:
             return jsonify({'message': 'friends list updated!'}),200
    else:
        postData={
            "userId":ObjectId(claims["id"]),
            "createdAt":datetime.now(),
            "pendingList":[xx]
        }
        updation=create_friends_list(postData)
        if updation==True:
            return jsonify({'message': 'friend added!'})
    
@friend_bp.route("/acceptRequest",methods=["POST"])
@jwt_required()
def accept_request():
    data=request.get_json()
    claims=get_jwt()
    uuid=claims["id"]
    userdata=find_user_byid(uuid)
    friends_data={
        "userId":ObjectId(data['userId']),
        "name":data["name"],
        "time":datetime.now(),
        "image":data["image"]
    }
    obj={
        "userId":ObjectId(uuid),
        "name":userdata['fullname'],
        "time":datetime.now(),
        "friendList":[friends_data]
    }
    pendinguser=find_friends_list(uuid)
    
    if pendinguser:
        pop_pending_req(uuid,data['userId'])

    xx=find_friends_list_data(uuid)
    if xx:
        #push the object into document freindlist array
        pushfriends=update_friend_list_data(friends_data,uuid)
        if pushfriends:
             return jsonify({'message': 'friend added!'}),200
    else:
        newdoc=create_friends_list_data(obj)
        if newdoc:
            return jsonify({"message":"Accepted"}),200


@friend_bp.route("/getFriendList",methods=["GET"])
@jwt_required()
def getFriendList():
    claims = get_jwt()
    userId = claims['id']
    friends = getFriendsList(userId)
    if friends:
        return jsonify(friends), 200
    else:
        return jsonify({'message': 'Lets explore some peoples !'}), 200


