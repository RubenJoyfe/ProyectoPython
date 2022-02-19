from ast import Pass
from hashlib import md5, new
from turtle import update
from unittest import result
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB+Compass&ssl=false')
db = client.Chaython



#--------------------------------------------------------- Rooms ---------------------------------------------------------
def createRoom(name, userId):
    room = {
        "_id": GetNextId('Rooms'),
        "name": name,
        "user_id": userId
    }





#--------------------------------------------------------- Users ---------------------------------------------------------
def registerUser(name, passwd):
    user =  {
    "_id": GetNextId('Users'),
    "name": name,
    "pass": md5(passwd.encode()).hexdigest(),
    }
    userNames = [u['name'] for u in getListOf('Users')]
    return -1 if name in userNames else db.Users.insert_one(user).inserted_id

def logIn(name, passwd):
    userList = getListOf('Users')
    for u in userList:
        if u['name'] == name and u['pass'] == md5(passwd.encode()).hexdigest():
            return u['_id']
    return -1

def getUserId(name):
    for u in getListOf('Users'):
        if u['name'] == name:
            return u['_id']
    return -1

def getListOf(collection):
    newList = [newList.append(p) for p in db[collection].find()]
    return newList

#--------------------------------------------------------- Otro ---------------------------------------------------------
def GetNextId(collection):
    return 0 if db[collection].count_documents({}) == 0 else db[collection].find().sort('_id', -1).limit(1)[0]['_id'] + 1


# print(registerUser('Alan2', 'uiiiii'))
# print(logIn('Alan2', 'uiiiii'))
# print(getUserId('Alan2'))
















# new_user =  {
#     "_id": GetLastId('Users') + 1,
#     "name": "Chayton",
#     "password": md5("1234".encode()).hexdigest(),
# }
# result = db.Users.insert_one(new_user)
# print(result)

# filter = {'user': 'admin'}
# projection = {}
# user = db.test.find_one(filter, projection)
# print(user)



# filter = {}
# projection = {'user': 1, '_id': 0}
# users = db.test.find(filter, projection)
# for u in users:
#     print(u)

# # Creamos un usuario

# # Borramos el usuario que acabamos de insertar
# filter = {'nick': 'admin1'}
# result = db.test.delete_one(filter)
# print(result.deleted_count)

# # Actualizamos el usuario
# filter = {'nick': 'admin1'}
# update = {'$set': {'nick': 'admin', 'login': True}}
# result = db.test.update_one(filter, update)

#





# msg = {
#     "_id": 1,
#     "room_id": 1,
#     "user_id": 1,
#     "message": "Hola, soy Chayton",
#     "date": "2020-01-01 00:00:00"
# }

# room = {
#     "_id": 1,
#     "name": "Chayton First Room",
# }