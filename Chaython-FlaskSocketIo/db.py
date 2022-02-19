from hashlib import md5
from turtle import update
from unittest import result
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB+Compass&ssl=false')

db = client.Chaython

def GetLastId(collection):
    return db[collection].find().sort('_id', -1).limit(1)[0]['_id']

# new_user =  {
#     "_id": GetLastId('Users') + 1,
#     "name": "Chayton",
#     "password": md5("1234".encode()).hexdigest(),
# }
# result = db.Users.insert_one(new_user)
# print(result.inserted_id)


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

user =  {
    "_id": 1,
    "name": "Chayton",
    "password": "1234"
}

msg = {
    "_id": 1,
    "room_id": 1,
    "user_id": 1,
    "message": "Hola, soy Chayton",
    "date": "2020-01-01 00:00:00"
}

room = {
    "_id": 1,
    "name": "Chayton First Room",
}