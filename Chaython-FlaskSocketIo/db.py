from dataclasses import asdict
import string
import random
import json
from ast import Pass
from hashlib import md5, new
from textwrap import indent
from turtle import update
from unittest import result
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB+Compass&ssl=false')
db = client.Chaython



#--------------------------------------------------------- Rooms ---------------------------------------------------------
# def createRoom(name, userId):
#     if not userId in [id['_id'] for id in getListOf('Users')]:
#         return -1

#     roomId = id_generator()
#     while(roomId in [id['_id'] for id in getListOf('Rooms')]):
#         roomId = id_generator()

#     room = {
#         "_id": roomId,
#         "name": name,
#         "user_id": userId,
#         "active": True
#     }
#     return db.Rooms.insert_one(room).inserted_id

#--------------------------------------------------------- Rooms ---------------------------------------------------------
def createRoom(name, userId):
    if getDocumentById('Users', userId) == None:
        return -1

    roomId = id_generator()
    while(getDocumentById('Rooms', roomId) != None):
        roomId = id_generator()

    room = {
        "_id": roomId,
        "name": name,
        "user_id": userId,
        "active": True
    }
    return db.Rooms.insert_one(room).inserted_id

def setRoomActive(roomId, active = True):
    room = getDocumentById('Rooms', roomId)
    if room == None: return -1
    room['active'] = active
    return  db.Rooms.update_one({'_id': roomId}, {'$set': room}).raw_result

def getRoomsByUser(userId):
    return [r for r in db.Rooms.find({'user_id': userId}, {})]

#--------------------------------------------------------- Users ---------------------------------------------------------
def registerUser(name, passwd):
    user =  {
    "_id": GetNextId('Users'),
    "name": name,
    "pass": md5(passwd.encode()).hexdigest(),
    }
    return -1 if db.Users.find_one({'name': name}, {}) == None else db.Users.insert_one(user).inserted_id

def logIn(name, passwd):
    return db.Users.find_one({'name': name, 'pass': passwd}, {})

def getUserId(name):
    user = db.Users.find_one({'name': name}, {})
    return -1 if user == None else user['_id']


#--------------------------------------------------------- Otro ---------------------------------------------------------
def getDocumentById(collection, id):
    return db[collection].find_one({'_id': id}, {})

def getListOf(collection):
    return [p for p in db[collection].find()]

def GetNextId(collection):
    return 0 if db[collection].count_documents({}) == 0 else db[collection].find().sort('_id', -1).limit(1)[0]['_id'] + 1

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# print(registerUser('Alan2', 'uiiiii'))
# print(logIn('Alan2', 'uiiiii'))
# print(getUserId('Alan2'))
# createRoom('rumsita buena', 3)
# print(getCollectionById('Users', 4))
# print(getListOf('Rooms'))
# print(setRoomActive('MXB3I6', False))
# createRoom('room0', 0)
# createRoom('room1', 0)
# createRoom('room2', 1)
# createRoom('room3', 0)
print(json.dumps(getRoomsByUser(1), indent = 4))









# # Creamos un usuario

# # Borramos el usuario que acabamos de insertar
# filter = {'nick': 'admin1'}
# result = db.test.delete_one(filter)
# print(result.deleted_count)

# # Actualizamos el usuario
# filter = {'nick': 'admin1'}
# update = {'$set': {'nick': 'admin', 'login': True}}
# result = db.test.update_one(filter, update)

# filter = {'user': 'admin'}
# projection = {}
# user = db.test.find_one(filter, projection)
# print(user)

#





# msg = {
#     "_id": 1,
#     "room_id": 1,
#     "user_id": 1,
#     "message": "Hola, soy Chayton",
#     "date": "2020-01-01 00:00:00"
# }
