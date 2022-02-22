from ast import If
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


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ContraseñaSuperSecretaQuenodeberíaSaberNADIE:=)'
app.config['SESSION_TYPE'] = 'filesystem'
JSON_KEY = 'ContraseñaSuperSecretaQuenodeberíaSaberNADIE:=)'

Session(app)

socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)
# socketio = SocketIO(app, manage_session=False)

def check_auth(redirect_name:str):
    def decorator(f:str):
        @wraps(f)
        def wrapper(*args, **kargs):
            try:
                if(session.get('name') is None):
                    return redirect(url_for('index'))
                elif (redirect_name != ''):
                    return redirect(url_for(redirect_name))
            except Exception as e:
                abort(401)
            pass
        return wrapper
    return decorator

@app.route('/', methods=['GET', 'POST'])
def index():
    if(session.get('name') is not None):
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if(session.get('name') is not None):
        return render_template('home.html', session = session) # return redirect(url_for('chat'))
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if(session.get('name') is not None):
        return redirect(url_for('home'))
    elif (request.method=='POST' and request.form['name'] is not None and request.form['password'] is not None):
        uname = request.form['name']
        pword = request.form['password']
        u = db.logIn(uname, pword)
        if u is None:
            # print(db.registerUser(uname, pword))
            return redirect(url_for('index')+'?error=1')
        user_chats = [{"name": "luk chat"}, {"name": "carl chat"}]
        token = jwt.encode({"id": u['_id'],"name": u['name']}, JSON_KEY, algorithm='HS256')
        session['name'] = uname
        session['chats'] = user_chats
        session['token'] = token
        # jsonify({"name": uname,"token": token}), 200
        return redirect(url_for('home'))
    return redirect(url_for('index'))

@app.route('/Chaython', methods=['GET', 'POST'])
def chat():
    if (session.get('name') is not None and request.form['room'] is not None):
        session['room'] = request.form['room']
        return render_template('chat.html', session = session)
    else:
        return redirect(url_for('index'))

# ("/user/<int:user_id>", methods=['GET'])
@socketio.on('join', namespace='/Chaython')
def join(message):
    if (session['room'] is None or session['room'] == ''):
        return redirect(url_for('home'))
    room:str = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('name') + ' has entered the room.'}, room=room)
    return render_template('chat.html', session = session)

@socketio.on('text', namespace='/Chaython')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ' : ' + message['msg']}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    username = session.get('username')
    room = session.get('room')
    leave_room(room)
    session['room'] = ''
    emit('status', {'msg': username + ' has left the room.'}, room=room)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
