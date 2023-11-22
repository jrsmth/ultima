import socketio
from flask import session, Blueprint
from flask_socketio import emit


# Socket Logic
def construct_blueprint(socket, redis):
    socket_page = Blueprint('socket_page', __name__)

    @socket.event
    def my_event(message):
        print('my_event')
        session['receive_count'] = session.get('receive_count', 0) + 1
        print(str(message))
        emit('my_response', {'data': message['data'], 'count': session['receive_count']})

    # Closing return
    return socket_page
