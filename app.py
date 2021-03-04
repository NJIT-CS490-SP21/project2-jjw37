import os
from flask import Flask, send_from_directory, json, session
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

APP = Flask(__name__, static_folder='./build/static')

CORS = CORS(APP, resources={r"/*": {"origins": "*"}})

USER_LIST = []
COUNTER = 0
USERS = []
LEADER_BOARD = {}

APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(APP)

import models
DB.create_all()


SOCKETIO = SocketIO(
    APP,
    cors_allowed_origins="*",
    json=json,
    manage_session=False
)

@APP.route('/', defaults={"filename": "index.html"})
@APP.route('/<path:filename>')
def index(filename):
    return send_from_directory('./build', filename)


@SOCKETIO.on('connect')
def on_connect():
    print('User connected!')

@SOCKETIO.on('disconnect')
def on_disconnect():
    print('User disconnected!')

@SOCKETIO.on('login')
def on_login(data):
    print(str(data))
    global USER_LIST
    global COUNTER
    global LEADER_BOARD
    leader_board_name = []
    leader_board_score = []
    db_query = models.Player.query.order_by(models.Player.score.desc()).all()
    for row in db_query:
        LEADER_BOARD[row.username] = row.score
    if data['userName'] not in LEADER_BOARD:
        db_user = models.Player(username=data['userName'], score=100)
        DB.session.add(db_user)
        DB.session.commit()
        LEADER_BOARD[data['userName']] = 100
    print(LEADER_BOARD)
    for name in LEADER_BOARD:
        leader_board_name.append(name)
        leader_board_score.append(LEADER_BOARD[name])
    print(leader_board_name)
    print(leader_board_score)
    if data['userName'] not in USER_LIST:
        USER_LIST.append(data['userName'])
    else:
        return
    global USERS
    COUNTER = COUNTER + 1
    if COUNTER == 1:
        USERS.append("Player X " + data['userName'])
    if COUNTER == 2:
        USERS.append("Player O " + data['userName'])
    if COUNTER > 2:
        USERS.append("spectator " + data['userName'])
    print(USER_LIST)
    SOCKETIO.emit('login', {'users': USERS, 'leaderBoardName': leader_board_name, 'leaderBoardScore': leader_board_score})
    SOCKETIO.emit('user_count', {'counter': COUNTER}, broadcast=False, include_self=True)


@SOCKETIO.on('restart')
def on_restart(data):
    print(str(data))
    SOCKETIO.emit('restart', data, broadcast=True, include_self=False)

@SOCKETIO.on('move')
def on_move(data):
    print(str(data))
    SOCKETIO.emit('move', data, broadcast=True, include_self=False)

SOCKETIO.run(
    APP,
    host=os.getenv('IP', '0.0.0.0'),
    port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
)
