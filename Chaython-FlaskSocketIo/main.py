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
# socketio = SocketIO(app, cors_allowed_origins="http://localhost")
JSON_KEY = 'ContraseñaSuperSecretaQuenodeberíaSaberNADIE:=)'

Session(app)

# socketio = SocketIO(app, manage_session=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if(session.get('name') is not None):
        return render_template('chat.html', session = session) # return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/Chaython', methods=['GET', 'POST'])
def chat():
    if (request.method=='POST'):
        uname = request.form['name']
        pword = request.form['password']
        token = jwt.encode({"id": str(""),"name": uname}, JSON_KEY, algorithm='HS256')
        session['name'] = uname
        session['token'] = token
        # jsonify({"name": uname,"token": token}), 200
        return render_template('chat.html', session = session)
    else:
        if (session.get('name') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))
        # return render_template('index.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

# @socketio.on('message')
# def handleMessage(msg):
#     print('Message: ' + msg)
#     send(msg, broadcast = True)

if __name__ == '__main__':
    app.run()
