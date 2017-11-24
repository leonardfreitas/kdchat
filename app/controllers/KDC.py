from flask import render_template, request, redirect, url_for
from app import app, socketio, db
from flask_login import login_required, current_user
from app.models.user import User, Room
from flask_socketio import join_room
import json
from flask import jsonify
import secrets
import random
from app.services.generate import gen, decrypt

roons_sid = []

@app.route("/chat")
@login_required
def index():
    return render_template('chatPage.html')


@socketio.on('event')
def handle_my_custom_event(json):
    print('RECEBIDO: ' + str(json))
    socketio.emit('response', json)


@socketio.on('connected')
def connected():
    socketio.emit('response_solicitation', 'CONNECTED')


@socketio.on('solicitation')
def KDC(info):
    data = json.dumps(info)
    dict_users = json.loads(data)
    requesting_client = User.query.filter_by(username=dict_users.get('requesting_client')).first()
    required_client = User.query.filter_by(username=dict_users.get('required_client')).first()
    if requesting_client == current_user and required_client:
        token_room = secrets.token_hex(nbytes=random.randint(50, 150))
        r1_token = gen(token_room, requesting_client.token)
        r1 = Room(token_room, r1_token, requesting_client.id)
        db.session.add(r1)
        r2_token = gen(token_room, required_client.token)
        r2 = Room(token_room, r2_token, required_client.id)
        db.session.add(r2)
        db.session.commit()
        socketio.emit('msg', {'status': '200'}, room=request.sid)


@socketio.on('conection')
def conection(id_sol):

    data = json.dumps(id_sol)
    dict_data = json.loads(data)
    room = Room.query.filter_by(id=dict_data['id']).first()
    token_crypt = room.token_room
    token_decrypt = decrypt(current_user.token, token_crypt)[1]
    if token_decrypt == room.public_key:
        socketio.emit('redirect', {'url': '/chat'})


