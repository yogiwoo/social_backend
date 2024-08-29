from flask import Blueprint,jsonify,request
from datetime import datetime
from pymongo import MongoClient
from app.utils.mongo import collection
from app.models.posts import insertPost,updateData,delete,hide,findPosts
from app.models.friends import find_friends_list_data
from flask_jwt_extended import get_jwt_identity,get_jwt,jwt_required
post_bp=Blueprint('post',__name__)
from bson import ObjectId
from app.utils.helper import parse_json,serialize_doc,convertObjectid
client=MongoClient("mongodb://localhost:27017/")
db = client["social"]
collection = db.posts
interaction_coll=db.interactions
@post_bp.route('/createPost',methods=['POST'])
@jwt_required()
def createPost():
    data=request.get_json()
    claims = get_jwt()
    userid = claims["id"]
    postImages=data.get("images")
    postText=data.get("text")
    postDate=datetime.now()
    userIdObject=ObjectId(userid)
    params={
        "userId":userIdObject,
        "postDate":postDate,
        "images":postImages, 
        "story":postText,
        "isHidden":False,
        "upvotes":0,
    }
    success=insertPost(params)
    if success:
        return jsonify({"message":"Posted"}),200
    else:
        return jsonify({"message":"Post failed"}),500

#update post
@post_bp.route('/updatePost',methods=["PUT"])
@jwt_required()
def updatePost():
     print("hi from update api")
     postId=request.args.get('pid')
     data=request.get_json()
     update=updateData(data,postId)
     if update:
         return jsonify({"message":"Posted update"}),200
     else:
         return jsonify({"message":"error"}),200

#delete post
@post_bp.route('/deletePost',methods=["DELETE"])
@jwt_required()
def deletePost():
    postId=request.args.get("pid")
    deletedata=delete(postId) 
    if deletedata==True:
        return jsonify({"message":"Post Deleted"}),200
    else:
        return jsonify({"message":"Failed"}),200

@post_bp.route('/hidePost/<int:pid>',methods=["PUT"])
@jwt_required()
def hidePost(pid):
    hide=hide(pid)
    if hide==True:
        return jsonify({"message":"Posted is now hidden"}),200
    else:
        return jsonify({"message":"Posted is not hidden"}),400

@post_bp.route("/fetch_timeline",methods=["GET"])
@jwt_required()
def fetch_post():
    #fetch friends userids
    claims=get_jwt()
    userid=claims["id"]
    friends=find_friends_list_data(userid)
    allposts=[]
    if(friends):
        for i in friends["friendList"]:
            uid=convertObjectid(i["userId"])
            post=collection.find({"userId.$oid":uid})
           
            for i in post:
                print("0000000000000000000000",i)
                searial=serialize_doc(i)
                allposts.append(searial)
    return allposts

@post_bp.route("/upvotePost/<int:pid>",methods=["PUT"])
@jwt_required()
def upvote():
    claims=get_jwt(pid)
    userid=claims["id"]
    #update upvotecounter 
    #insert userid in the interactions collection for the post
    pid=request.args.get["pid"]
    updateUpvotes=collection.update_one({"_id"},{"$inc":{"upvotes":1}})
    if updateUpvotes:
        object={
            "userId":ObjectId(userid),
            "upvotedBy":""
        }
        insertInteraction=interaction_coll.insert_one()