from dataclasses import asdict
import string
from datetime import datetime
import random
import json
import operator
from ast import Pass
from hashlib import md5, new
from textwrap import indent
from turtle import update
from unittest import result
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB+Compass&ssl=false')
db = client.Chaython


#--------------------------------------------------------- Messages ---------------------------------------------------------

def createMessageChat(userId, chatId, msg, date = datetime.now()):
    chat = getDocumentById("Chats", chatId)
    user = getDocumentById("Users", userId)
    if chat is None: return -1
    if user is None: return -2
    if userId not in chat["users"]: return -3
    if chat is None or user is None or userId not in chat["users"]: return -1
    message = {
        "_id": GetNextId("Messages"),
        "user_id": userId,
        "chat_id": chatId,
        "room_id": None,
        "message": msg,
        "date": date
    }
    return db.Messages.insert_one(message).inserted_id

def createMessageRoom(userId, roomId, msg, date = datetime.now()):
    room = getDocumentById("Rooms", roomId)
    user = getDocumentById("Users", userId)
    if room is None: return -1
    if user is None: return -2
    if userId not in room["users"]: return -3
    message = {
        "_id": GetNextId("Messages"),
        "user_id": userId,
        "chat_id": None,
        "room_id": roomId,
        "message": msg,
        "date": date
    }
    return db.Messages.insert_one(message).inserted_id

def getMessagesByChat(chatId):
    if getDocumentById("Chats", chatId) is None: return -1
    l = [ m for m in db.Messages.find({'chat_id': chatId}, {})]
    l.sort(key=operator.itemgetter('date'))
    for m in l:
        m["name"] = getDocumentById("Users", m["user_id"])["name"]
    return l

def getMessagesByRoom(roomId):
    if getDocumentById("Rooms", roomId) is None: return -1
    l = [ m for m in db.Messages.find({'room_id': roomId}, {})]
    l.sort(key=operator.itemgetter('date'))
    for m in l:
        m["name"] = getDocumentById("Users", m["user_id"])["name"]
    return l

#--------------------------------------------------------- Chats ---------------------------------------------------------

def createChat(users):
    if len(users) < 2: return -1
    if users[0] == users[1]: return -2
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

def getChatsByUser(userId):
    chats = []
    for c in db.Chats.find():
        if userId in c['users']:
            other = c['users'][0] if c['users'][0] != userId else c['users'][1]
            c["otherUserId"] = other
            c["otherUserName"] = getDocumentById("Users", other)["name"]
            chats.append(c)
    return chats

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
    return 1000 if db[collection].count_documents({}) == 0 else db[collection].find().sort('_id', -1).limit(1)[0]['_id'] + 1

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



registerUser("crami", "1234")
registerUser("luk", "1234")