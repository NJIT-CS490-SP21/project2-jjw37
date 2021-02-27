import os
from flask import Flask, send_from_directory, json, session
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__, static_folder='./build/static')

cors = CORS(app, resources={r"/*": {"origins": "*"}})

userList = []
counter = 0
users = []

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    json=json,
    manage_session=False
)

@app.route('/', defaults={"filename": "index.html"})
@app.route('/<path:filename>')
def index(filename):
    return send_from_directory('./build', filename)

@socketio.on('connect')
def on_connect():
    print('User connected!')

@socketio.on('disconnect')
def on_disconnect():
    print('User disconnected!')
    
@socketio.on('login')
def on_login(data):
    print(str(data))
    global userList
    global counter
    if data['userName'] not in userList:
        userList.append(data['userName'])
    else:
        return
    global users 
    counter = counter + 1
    if counter == 1:
        users.append("Player X " + data['userName'])
    if counter == 2:
        users.append("Player O " + data['userName'])
    if counter > 2:
        users.append("spectator " + data['userName'])
    print(userList)
    socketio.emit('login', {'users': users})
    socketio.emit('user_count', {'counter': counter}, broadcast=False, include_self=True)
    
    
@socketio.on('restart')
def on_restart(data): 
    print(str(data))
    socketio.emit('restart',  data, broadcast=True, include_self=False)

@socketio.on('move')
def on_move(data): 
    print(str(data))
    socketio.emit('move',  data, broadcast=True, include_self=False)

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
)
