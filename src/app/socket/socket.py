from flask import Blueprint
from flask_socketio import join_room, emit


# Socket Logic
def construct_blueprint(socket):
    socket_page = Blueprint('socket_page', __name__)

    @socket.on('join')
    def on_join(data):
        user_id = data['userId']
        room = data['gameId']
        join_room(room)

        trigger = user_id + ' has entered the room for game with id: ' + room
        print(f"[on_join] {trigger}")
        emit('connected', trigger, to=room)

    # Blueprint return
    return socket_page
