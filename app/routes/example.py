from flask import Blueprint,request,jsonify
from app.utils.mongo import collection
from app.models.example import get_all_items,add_item

example_bp=Blueprint('example',__name__)


@example_bp.route('/',methods=["GET"])
def default_path():
    return jsonify({"Message":"Welcome"})

@example_bp.route('/items',methods=["GET"])
def get_items():
    items = get_all_items()
    return jsonify(items)

@example_bp.route('/additems',methods=["POST"])
def add_items():
    data=request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'Missing "text" field'}), 400
    text = data['text']
    add_item(text)
    return jsonify({'message': 'Item added successfully!'})