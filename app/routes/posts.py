from flask import Blueprint,jsonify,request
from app.utils.mongo import collection
from app.models.posts import insertPost

post_bp=Blueprint('post',__name__)


@post_bp.route('/createPost',methods=['POST'])
def createPost():
    data=req.get_json()
    