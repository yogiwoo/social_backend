from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import objectId
app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["course-goals"]
collection = db.goals


@app.route('/',methods=["GET"])
def defaultPath():
    return jsonify({"Message":"Welcome"})
@app.route('/items', methods=['GET'])
def get_items():
    items =list(collection.find({},{'_id':False}))
    return jsonify(items)


@app.route('/additems',methods=['POST'])
def addItems():
    data =request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'Missing "text" field'}), 400
    text =data['text']
    collection.insert_one({'text': text})
    return jsonify({'message': 'Item added successfully!'})
    
if __name__ == '__main__':
    #automatically restarts app when change in dev mode 
    app.run(debug=True)
