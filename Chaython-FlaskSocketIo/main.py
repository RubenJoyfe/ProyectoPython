from ast import If
from asyncio.windows_events import NULL
from getpass import getuser
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from distutils.dep_util import newer
from datetime import datetime, timedelta
from functools import wraps
from itsdangerous import exc
import requests, json, os, jwt
#Mongo DB manager
import db
from bson.json_util import dumps
from bson.objectid import ObjectId


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ContraseñaSuperSecretaQuenodeberíaSaberNADIE:=)'
app.config['SESSION_TYPE'] = 'filesystem'
# JSON_KEY = 'ContraseñaSuperSecretaQuenodeberíaSaberNADIE:=)'

Session(app)

socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)
# socketio = SocketIO(app, manage_session=False)

def check_auth(session_item_name:str, redirect_name:str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kargs):
            try:
                if(session.get(session_item_name) is None):
                    return redirect(url_for(redirect_name))
                else: 
                    return f(*args, **kargs)
            except Exception as e:
                redirect(url_for('logout'))
                abort(401)
            pass
        return wrapper
    return decorator

@app.route('/', methods=['GET', 'POST'])
def index():
    if(session.get('name') is not None):
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/r', methods=['GET', 'POST'])
def reg():
    if(session.get('name') is not None):
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
@check_auth('name', 'index')
def home():
    # uid = session['uid']
    # session['chats'] = db.getRoomsByUser(uid)
    return render_template('home.html', session = session) # return redirect(url_for('chat'))

@app.route('/login', methods=['POST'])
def login():
    if(session.get('name') is not None):
        return redirect(url_for('home'))
    elif (request.form['name'] is not None and request.form['password'] is not None):
        uname = request.form['name']
        pword = request.form['password']
        u = db.logIn(uname, pword)
        if u is None:
            # print(db.registerUser(uname, pword))
            return redirect(url_for('index')+'?error=1')
        # token = jwt.encode({"id": u['_id'],"name": u['name']}, JSON_KEY, algorithm='HS256')
        # session['token'] = token
        session['uid'] = u['_id']
        session['name'] = uname
        session['user_code'] = u['code']
        # session['chats'] = db.getRoomsByUser(u['_id'])
        # jsonify({"name": uname,"token": token}), 200
        return redirect(url_for('home'))
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    if(session.get('name') is not None):
        return redirect(url_for('home'))
    elif (request.form['name'] is not None and request.form['password'] is not None):
        uname = request.form['name']
        pword = request.form['password']
        if pword != request.form['password2']:
            return redirect(url_for('reg')+'?error=11')
        u = db.registerUser(uname, pword)
        if u is None:
            return redirect(url_for('reg')+'?error=10')
        session['uid'] = u['_id']
        session['name'] = u['name']
        session['user_code'] = u['code']
        return redirect(url_for('home'))
    return redirect(url_for('reg'))

@app.route('/Chaython', methods=['GET', 'POST'])
@check_auth('name', 'home')
def chat():
    if (request.form['room'] is not None and request.form['room_action'] is not None):
        session['room'] = request.form['room']
        room_action = request.form['room_action']
        if(room_action == 'create'):
            session['room_key'] = db.createRoom(session['room'],session['uid'])['code']
        elif(room_action == 'join'):
            session['room_key'] = session['room']
            res = db.setUserToRoom(session['uid'], session['room_key'])
            if(res == -1):
                return redirect(url_for('home'))
            roomInfo = db.getRoomByCode(session['room_key'])
            session['room'] = roomInfo['name']
        return render_template('chat.html', session = session)
    elif (session.get('room_key') is not None and session.get('room_key') != ''):
        return render_template('chat.html', session = session)
    else:
        return redirect(url_for('index'))

@app.route('/Chaython/private', methods=['GET', 'POST'])
@check_auth('name', 'home')
def JoinPrivateChat():
    if (request.form['chat'] is None or request.form['chat'] == ''):
        return redirect(url_for('home'))
    if str(request.form['chat']) not in [str(c['_id']) for c in db.getChatsByUser(session['uid'])]:
        return redirect(url_for('home'))
    session['chat_key'] = request.form['chat']
    session['chat_name'] = request.form['connect_to']
    return render_template('private.html', session = session)

@app.route('/Chaython/', methods=['GET'])
def backToHome():
    return redirect(url_for('home'))

@app.route('/Chaython/<string:room_key>', methods=['GET'])
@check_auth('name', 'home')
def chatbyid(room_key):
    if (room_key is not None):
        session['room_key'] = room_key
        return render_template('chat.html', session = session)
    else:
        return redirect(url_for('home'))

@app.route('/rooms', methods=['GET'])
@check_auth('name', 'index')
def getRooms():
    return dumps(db.getRoomsByUser(session['uid']))

@app.route('/chats', methods=['GET'])
@check_auth('name', 'index')
def getChats():
    return dumps(db.getChatsByUser(session['uid']))

@app.route('/msgsroom/<string:id>', methods=['GET'])
@check_auth('name', 'index')
def getRoomMsgs(id):
    if id in [r['code'] for r in db.getRoomsByUser(session['uid'])]:
        return dumps(db.getMessagesByRoom(id))
    return redirect(url_for('home'))

@app.route('/msgschat/<string:id>', methods=['GET'])
@check_auth('name', 'index')
def getChatMsgs(id):
    if id in [str(c['_id']) for c in db.getChatsByUser(session['uid'])]:
        return dumps(db.getMessagesByChat(id))
    return redirect(url_for('home'))

# TODO: Numero personal + devolver el usuario
@app.route('/chat/<int:personalnumber>', methods=['GET'])
@check_auth('name', 'index')
def getPersonByPersonalNumber(personalnumber):
    return dumps(db.getUserByCode(personalnumber))

@app.route('/chat/add/<int:user_code>', methods=['GET'])
@check_auth('name', 'index')
def addPersonalChat(user_code):
    users = [session['user_code'], user_code]
    return dumps(db.createChat(users))

@socketio.on('join', namespace='/Chaython')
def join(message):
    wtf = 'Roboto-Regular.ttf'
    room_key = session.get('room_key') if session.get('room_key') != wtf else ''
    chat_key = session.get('chat_key') if session.get('chat_key') != wtf else ''
    if room_key is not None and room_key != '':
        #roomkey
        room_key = session['room_key']
        join_room(room_key)
        emit('status', {'msg':  session.get('name') + ' has entered the room.'}, room=room_key)
        return render_template('chat.html', session = session)
    elif chat_key is not None and chat_key != '':
        #chatkey
        chat_key = session['chat_key']
        join_room(chat_key)
        # emit('status', {'msg':  session.get('name') + ' has entered the chat.'}, room=room_key)
        return render_template('private.html', session = session)
    else:
        return redirect(url_for('home'))

@socketio.on('text', namespace='/Chaython')
def text(message):
    wtf = 'Roboto-Regular.ttf'
    room_key = session.get('room_key') if session.get('room_key') != wtf else ''
    chat_key = session.get('chat_key') if session.get('chat_key') != wtf else ''
    if room_key is not None and room_key != '':
        print('r:' + room_key)
        db.createMessageRoom(session['uid'], room_key, message.get("msg"))
        emit('message', {'msg': session.get('name') + ' : ' + message['msg']}, room=room_key)
    elif chat_key is not None and chat_key != '':
        print('c:' + chat_key)
        db.createMessageChat(session['uid'], chat_key, message.get("msg"))
        emit('message', {'msg': session.get('name') + ' : ' + message['msg']}, room=chat_key)
    else:
        redirect(url_for('home'))

@socketio.on('left', namespace='/Chaython')
def left(message):
    username = session.get('username')
    room_key = ''
    chat_key = ''
    if(session.get('room_key') is not None):
        room_key = session['room_key']
    if(session.get('chat_key') is not None):
        chat_key = session['chat_key']
    leave_room(room_key)
    leave_room(chat_key)
    session['room'] = ''
    session['room_key'] = ''
    session['chat_key'] = ''
    session['chat_name'] = ''

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
