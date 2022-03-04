from flask import Flask, request, jsonify;
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/sphilip3app'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users

@app.route('/users', methods=['POST'])
def createUser():
    id = db.insert({
        'name': request.json['name'],
        'ident': request.json['ident'],
        'points': request.json['points']
    })
    return jsonify({'id': str(ObjectId(id)), 'msg': 'User added.'})

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            'id': str(ObjectId(doc['_id'])),
            'name' : doc['name'],
            'ident' : doc['ident'],
            'points' : doc['points']
        })
        return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
    user = db.find_one({'id': ObjectId(id)})
    return jsonify({
        'id': str(ObjectId(user['_id'])),
        'name' : user['name'],
        'ident' : user['ident'],
        'points' : user['points']
    })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    db.delete_one({'id': ObjectId(id)})
    return jsonify('User deleted.')


@app.route('/users/<id>', methods=['PUT'])
def updateUsers(id):
    db.update_one({'id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'ident': request.json['ident'],
        'points': request.json['points']
    }})
    return jsonify('User updated.')

if __name__ == '__main__':
    app.run(debug=True)