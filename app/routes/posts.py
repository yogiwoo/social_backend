from flask import Blueprint,jsonify,request
from datetime import datetime
from app.utils.mongo import collection
from app.models.posts import insertPost,updateData,delete,hide,findPosts
from app.models.friends import find_friends_list_data
from flask_jwt_extended import get_jwt_identity,get_jwt,jwt_required
post_bp=Blueprint('post',__name__)
from bson import ObjectId
from app.utils.helper import parse_json,serialize_doc,convertObjectid
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
    users=[]
    if(friends):
        for i in friends["friendList"]:
            users.append(convertObjectid(i["userId"])) #serialize_doc

    allposts=findPosts(users)        
    return allposts