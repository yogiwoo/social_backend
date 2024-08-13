from flask import Blueprint,request,jsonify
from app.utils.mongo import collection
from app.models.auth import insert_user,find_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
from app.utils.helper import parse_json,serialize_doc
auth_bp=Blueprint('auth',__name__)
from config import Config
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from app.utils.helper import parse_json
from bson.json_util import dumps,loads
from bson import ObjectId
from flask_pymongo import PyMongo
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
    data=request.get_json()
    userdata=find_user(data.get('mobile'))
    if userdata:
        fullname=userdata.get('fullname')
        password=userdata.get('pwd')
        if check_password_hash(password,data.get('pwd')):
            token=create_access_token(identity=fullname)
            serialize_userdata=serialize_doc(userdata)
            return jsonify({'token':token,'userdata':serialize_doc}),200
    #final=parse_json(userdata)
    # serialized_userdata = dumps(userdata)
    # print("------------------------------------------------------------------------->",serialized_userdata)
    # if serialized_userdata:
    #     fullname=userdata.get('fullname')
    #     password=userdata.get('pwd')
    #     email=userdata.get('email')
    #     mobile=userdata.get('mobile')
    #     id=userdata.get('_id')
    #     if check_password_hash(password,data.get('pwd')):
            
    #         access_token = create_access_token(identity=fullname,additional_claims=additional_claims)
    #         return jsonify({'access_token': access_token,'user_data': serialized_userdata}), 200





