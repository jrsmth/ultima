import os

from flask import Flask
from flask_socketio import SocketIO

from src.app.config.config import Config, DevConfig, ProductionConfig
from src.app.game import game
from src.app.login import login
from src.app.socket import socket
from src.app.util.messages import Messages
from src.app.util.redis import Redis

# Initialise app
templates = os.path.abspath("../resources/templates")
statics = "../resources/static"
app = Flask(__name__, template_folder=templates, static_folder=statics)
socketio = SocketIO(app)

# Initialise config
env = os.environ.get("FLASK_ENV")

if not env:
    raise ValueError("Start-up failed: no environment specified!")
elif env == "local":
    app.config.from_object(Config())
    print("Starting app in [local] mode")
elif env == "dev":
    app.config.from_object(DevConfig())
    print("Starting app in [dev] mode")
elif env == "prod":
    app.config.from_object(ProductionConfig())
    print("Starting app in [production] mode")

# Initialise redis client
redis = Redis(app)

# Initialise message bundle
messages = Messages('../resources/messages.properties')

# Register routes
app.register_blueprint(login.construct_blueprint(messages, socketio, redis))
app.register_blueprint(game.construct_blueprint(messages, socketio, redis))

# Register events
app.register_blueprint(socket.construct_blueprint(socketio, redis))

# Let's go!
if __name__ == "__main__":
    socketio.run(app, debug=True, host='localhost', port=8080)  # FixMe :: extract
