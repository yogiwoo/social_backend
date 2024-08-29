from flask import Blueprint,jsonify,request
from datetime import datetime
from app.utils.mongo import collection
from app.models.friends import find_friends_list,create_friends_list,update_friend_list_pending,update_friend_list_data,find_friends_list_data,create_friends_list_data,pop_pending_req,getFriendsList
from flask_jwt_extended import get_jwt_identity,get_jwt,jwt_required
friend_bp=Blueprint('friend',__name__)
from app.utils.helper import parse_json,serialize_doc,convertObjectid
from bson import ObjectId
from app.models.auth import find_user,find_user_byid