import os
from flask import Flask, send_from_directory, json, session
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__, static_folder='./build/static')

cors = CORS(app, resources={r"/*": {"origins": "*"}})

<<<<<<< HEAD
=======
userList = []
counter = 0
users = []

>>>>>>> milestone_1
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

<<<<<<< HEAD
# When a client connects from this Socket connection, this function is run
=======
>>>>>>> milestone_1
@socketio.on('connect')
def on_connect():
    print('User connected!')

<<<<<<< HEAD
# When a client disconnects from this Socket connection, this function is run
@socketio.on('disconnect')
def on_disconnect():
    print('User disconnected!')

# When a client emits the event 'chat' to the server, this function is run
# 'chat' is a custom event name that we just decided
@socketio.on('chat')
def on_chat(data): # data is whatever arg you pass in your emit call on client
    print(str(data))
    # This emits the 'chat' event from the server to all clients except for
    # the client that emmitted the event that triggered this function
    socketio.emit('chat',  data, broadcast=True, include_self=False)

# Note that we don't call app.run anymore. We call socketio.run with app arg
=======
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

>>>>>>> milestone_1
socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
)