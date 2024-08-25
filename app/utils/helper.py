from bson import json_util
import json
def parse_json(data):
    return json.loads(json_util.dumps(data))

def serialize_doc(doc):
    doc['_id']=str(doc['_id'])
    return doc

def convertObjectid(id):
    return str(id)