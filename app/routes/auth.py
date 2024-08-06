from flask import Blueprint,request,jsonify
from app.utils.mongo import collection
from app.models.auth import insert_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
from app.utils.helper import parse_json
auth_bp=Blueprint('auth',__name__)

@auth_bp.route('/signup',methods=['POST'])
def signup():
    data=request.get_json()
    username=data.get('userName')
    password=data.get('pwd')
    email=data.get('email')
    mobile=data.get('mobile')
    hashed_password = generate_password_hash(password,  method='pbkdf2:sha256')
    hashed_password_value = hashed_password.split('$', 2)[-1]
    params={
       'fullname': username,
        'pwd': hashed_password_value,
        'mail': email,
        'mob': mobile
    }
    success=insert_user(params)
    if success:
        return jsonify({'message': 'Item added successfully!','data':params})
    else:
        return jsonify({"message":"Signup failed"})

