"""Server side code"""
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
WINNER_COUNT = 0

APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(APP)

import models

SOCKETIO = SocketIO(APP,
                    cors_allowed_origins="*",
                    json=json,
                    manage_session=False)


@APP.route('/', defaults={"filename": "index.html"})
@APP.route('/<path:filename>')
def index(filename):
    """Sending file"""
    return send_from_directory('./build', filename)


@SOCKETIO.on('connect')
def on_connect():
    """socket event for user connect"""
    print('User connected!')


@SOCKETIO.on('disconnect')
def on_disconnect():
    """socket event for user disconnect"""
    print('User disconnected!')

def add_user(user):
    """Adds user to USERS"""
    global USERS
    global COUNTER
    new_user = "Player X " + user
    if COUNTER == 1:
        new_user = "Player X " + user
        USERS.append("Player X " + user)
    if COUNTER == 2:
        new_user = "Player O " + user
        USERS.append("Player O " + user)
    if COUNTER > 2:
        new_user = "Spectator " + user
        USERS.append("spectator " + user)
    return new_user

@SOCKETIO.on('login')
def on_login(data):
    """returns current userlist and list of users from database with any new users added"""
    print(str(data))
    global USER_LIST
    global COUNTER
    global LEADER_BOARD
    leader_board_name = []
    leader_board_score = []
    try:
        db_query = models.Player.query.order_by(
            models.Player.score.desc()).all()
        for row in db_query:
            LEADER_BOARD[row.username] = row.score
        if data['userName'] not in LEADER_BOARD:
            db_user = models.Player(username=data['userName'], score=100)
            DB.session.add(db_user)
            DB.session.commit()
            LEADER_BOARD[data['userName']] = 100
    except:
        LEADER_BOARD['Man'] = 22
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
    add_user(data['userName'])
    print(USER_LIST)
    print(COUNTER)
    SOCKETIO.emit(
        'login', {
            'users': USERS,
            'leaderBoardName': leader_board_name,
            'leaderBoardScore': leader_board_score
        })
    SOCKETIO.emit('user_count', {'counter': COUNTER},
                  broadcast=False,
                  include_self=True)

def set_winner(players, is_winner):
    """sets the winner and loser"""
    winner_list = []
    if is_winner:
        print('winner is ' + players[1])
        winner = players[1]
        print('loser is ' + players[0])
        loser = players[0]
    if not is_winner:
        print('winner is ' + players[0])
        winner = players[0]
        print('loser is ' + players[1])
        loser = players[1]
    winner_list.append(winner)
    winner_list.append(loser)
    return winner_list

@SOCKETIO.on('winner')
def on_winner(data):
    """socket event for winner, updates database of winner/loser score, returns updated list"""

    board = {}
    winner_list = []
    board_name = []
    board_score = []
    global WINNER_COUNT
    print("The winner count in on winner is " + str(WINNER_COUNT))
    WINNER_COUNT = WINNER_COUNT + 1
    if WINNER_COUNT >= 2:
        return
    global USER_LIST
    player_list = USER_LIST
    winner_player = data['xNext']
    winner_list = set_winner(player_list, winner_player)
    winner = winner_list[0]
    loser = winner_list[1]
    print("steve")
    try:
        winner_qr = DB.session.query(
            models.Player).filter_by(username=winner).first()
        winner_qr.score = winner_qr.score + 1
        DB.session.commit()
        loser_qr = DB.session.query(
            models.Player).filter_by(username=loser).first()
        loser_qr.score = loser_qr.score - 1
        DB.session.commit()
        db_query = models.Player.query.order_by(
            models.Player.score.desc()).all()
        for row in db_query:
            board[row.username] = row.score
        for name in board:
            board_name.append(name)
            board_score.append(board[name])
    except:
        board_score = [12]
        board_name = ['bill']
    print(board)
    SOCKETIO.emit('updateBoard', {
        'boardName': board_name,
        'boardScore': board_score
    })


@SOCKETIO.on('restart')
def on_restart(data):
    """socket event for restart, resets the board of all players/spectators"""
    global WINNER_COUNT
    WINNER_COUNT = 0
    print("The winner count is " + str(WINNER_COUNT))
    print(str(data))
    SOCKETIO.emit('restart', data, broadcast=True, include_self=False)

def check_move(data):
    """checks and prints move"""
    print(str(data))
    return((data))

@SOCKETIO.on('move')
def on_move(data):
    """socket event for move, will display updated board to all players/spectators"""
    check_move(data)
    global WINNER_COUNT
    WINNER_COUNT = 0
    SOCKETIO.emit('move', data, broadcast=True, include_self=False)


if __name__ == "__main__":
    DB.create_all()
    SOCKETIO.run(
        APP,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )
