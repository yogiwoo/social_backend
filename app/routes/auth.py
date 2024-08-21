from flask import Blueprint,request,jsonify
from app.utils.mongo import collection
from app.models.auth import insert_user,find_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest
import json
from datetime import datetime
from app.utils.helper import parse_json,serialize_doc
auth_bp=Blueprint('auth',__name__)
from config import Config
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity,get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from app.utils.helper import parse_json
from bson.json_util import dumps,loads
from bson import ObjectId
from flask_pymongo import PyMongo
from datetime import timedelta
@auth_bp.route('/signup',methods=['POST'])
def signup():
    data=request.get_json()
    username=data.get('userName')
    password=data.get('pwd')
    email=data.get('email')
    mobile=data.get('mobile')
    img=data.get('img')
    hashed_password = generate_password_hash(password,  method='pbkdf2:sha256')
    #hashed_password_value = hashed_password.split('$', 2)[-1]
    params={
        'fullname': username,
        'pwd': hashed_password,
        'mail': email,
        'mob': mobile,
        'profilePic':img,
        'Active':True,
        'joinedAt':datetime.now(),
    }
    success=insert_user(params)
    if success:
        return jsonify({'message': 'Item added successfully!','data':params})
    else:
        return jsonify({"message":"Signup failed"})

@auth_bp.route('/login',methods=["POST"])
def login():
    try:
        data=request.get_json()
        userdata=find_user(data.get('mobile'))
        if userdata:
            fullname=userdata.get('fullname')
            password=userdata.get('pwd')
            if check_password_hash(password,data.get('pwd')):
                print("---------------------------------------------------->")
                serialize_userdata=serialize_doc(userdata)
                print(serialize_userdata)
                token=create_access_token(identity=fullname,expires_delta=timedelta(hours=4), additional_claims={
                "id": serialize_userdata.get('_id'),
                "mobile": serialize_userdata.get('mob')
            })   
        return jsonify({'token':token,'userdata':serialize_userdata}),200
    except BadRequest as e:
        return jsonify({'error':str(e)}),400

@auth_bp.route('/searchuser',methods=["GET"])
@jwt_required()
def searchUser():
        try:
            curr_user=get_jwt_identity()
            claims = get_jwt() 
            print('current user---------->',claims["id"])
            return jsonify({'current_user': curr_user,"id":claims["id"]}), 200
        except :
            return ("error")






