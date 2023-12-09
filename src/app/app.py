import json
import logging
import os
from logging.config import dictConfig

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_socketio import SocketIO
from from_root import from_root

from src.app.admin import admin
from src.app.config.config import Config, DevConfig, ProductionConfig
from src.app.game import game
from src.app.login import login
from src.app.socket import socket
from src.app.util.messages import Messages
from src.app.util.redis import Redis


# Initialise app
templates = from_root("resources", "templates")
statics = from_root("resources", "static")
app = Flask(__name__, template_folder=templates, static_folder=statics)
socketio = SocketIO(app)
auth = HTTPBasicAuth()


# Initialise config
env = os.environ.get("FLASK_ENV")

if not env:
    raise ValueError("Start-up failed: no environment specified!")
elif env == "local":
    app.config.from_object(Config())
elif env == "dev":
    app.config.from_object(DevConfig())
elif env == "prod":
    app.config.from_object(ProductionConfig())
print(f"Starting app in [{env}] mode")
app.app_context().push()


# Initialise redis client
redis = Redis(app)


# Initialise message bundle
messages = Messages(from_root('resources', 'messages.properties'))


# Initialise logger
dictConfig(json.load(open(from_root('app', 'config', 'logs.json'))))
app.logger_name = 'ultima'


# Register routes
app.register_blueprint(admin.construct_blueprint(auth, redis))
app.register_blueprint(login.construct_blueprint(messages, redis))
app.register_blueprint(game.construct_blueprint(messages, redis, socketio))


# Register events
app.register_blueprint(socket.construct_blueprint(socketio))


# Let's go!
if __name__ == "__main__":
    socketio.run(app, debug=True, host='localhost', port=8080)  # FixMe :: extract
