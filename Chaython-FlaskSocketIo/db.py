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
msg = {
    "_id": 1,
    "room_id": 1,
    "user_id": 1,
    "message": "Hola, soy Chayton",
    "date": "2020-01-01 00:00:00"
}

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


#--------------------------------------------------------- Chats ---------------------------------------------------------


def createChat(users):
    if len(users) < 2: return -1
    if getDocumentById("Users", users[0]) is None or getDocumentById("Users", users[1]) is None: return -2
    users = users[0:2]
    users.sort()

    chat = db.Chats.find_one({'users': users}, {})
    if chat is not None: return chat["_id"]

    chat = {
        "_id": GetNextId("Chats"),
        "users": users
    }
    return db.Chats.insert_one(chat).inserted_id


#--------------------------------------------------------- Rooms ---------------------------------------------------------
def createRoom(name, firstUserId):
    if getDocumentById('Users', firstUserId) == None:
        return -1

    roomId = id_generator()
    while(getDocumentById('Rooms', roomId) != None):
        roomId = id_generator()

    room = {
        "_id": roomId,
        "name": name,
        "users": [firstUserId],
        "active": True
    }
    return db.Rooms.insert_one(room).inserted_id

def setRoomActive(roomId, active = True):
    room = getDocumentById('Rooms', roomId)
    if room == None: return -1
    room['active'] = active
    return  db.Rooms.update_one({'_id': roomId}, {'$set': room}).raw_result

def getRoomsByUser(userId):
    rooms = []
    for r in db.Rooms.find():
        if userId in r['users']:
            rooms.append(r)
    return rooms

def setUserToRoom(userId, roomId, remove = False):
    room = getDocumentById('Rooms', roomId)
    if room is None or getDocumentById('Users', userId) is None:
        return -1
    if remove:
        if userId in room["users"]:
            room['users'].remove(userId)
        else:
            return -2
    else:
        if not userId in room['users']: room['users'].append(userId)
    return  db.Rooms.update_one({'_id': roomId}, {'$set': room}).raw_result

def changeRoomName(roomId, name):
    room = getDocumentById('Rooms', roomId)
    if room is None: return -1
    room["name"] = name
    return  db.Rooms.update_one({'_id': roomId}, {'$set': room}).raw_result

#--------------------------------------------------------- Users ---------------------------------------------------------
def registerUser(name, passwd):
    user =  {
    "_id": GetNextId('Users'),
    "name": name,
    "pass": md5(passwd.encode()).hexdigest(),
    }
    return -1 if db.Users.find_one({'name': name}, {}) != None else db.Users.insert_one(user).inserted_id

def logIn(name, passwd):
    return db.Users.find_one({'name': name, 'pass': md5(passwd.encode()).hexdigest()}, {})

def getUserId(name):
    user = db.Users.find_one({'name': name}, {})
    return -1 if user == None else user['_id']


#--------------------------------------------------------- Otro ---------------------------------------------------------
def getDocumentById(collection, id):
    return db[collection].find_one({'_id': id}, {})

def getListOf(collection):
    return [p for p in db[collection].find()]

def GetNextId(collection):
    return 1 if db[collection].count_documents({}) == 0 else db[collection].find().sort('_id', -1).limit(1)[0]['_id'] + 1

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# print(registerUser('Alan1', '1234'))
# print(registerUser('Alan2', '1234'))
# print(registerUser('Alan3', '1234'))
# print(logIn('Alan2', 'uiiiii'))
# print(getUserId('Alan2'))
# createRoom('rumsita buena', 3)
# print(getCollectionById('Users', 4))
# print(getListOf('Rooms'))
# print(setRoomActive('MXB3I6', False))
# print(createRoom('room0', 0))
# print(createRoom('room1', 0))
# print(createRoom('room2', 1))
# print(createRoom('room3', 0))
# print(json.dumps(getRoomsByUser(1), indent = 4))
# print(setUserToRoom(2, 'W1TCIQ'))

# print(createChat([1,2,3,4]))
# print(createChat([2,1]))
# print(createChat([1]))
# print(createChat([2,6]))









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
