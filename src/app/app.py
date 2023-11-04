import os
from flask import Flask
from src.app.config.config import Config, DevConfig, ProductionConfig
from src.app.game import game
from src.app.login import login
from src.app.util.messages import load_messages
from src.app.util.redis import init_redis


# Initialise app
templates = os.path.abspath("../resources/templates")
statics = "../resources/static"
app = Flask(__name__, template_folder=templates, static_folder=statics)


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
client = init_redis(app)


# Initialise message bundle
messages = load_messages()


# Register routes
app.register_blueprint(login.construct_blueprint(client, messages))
app.register_blueprint(game.construct_blueprint(client, messages))


# Let's go!
if __name__ == "__main__":
    app.run()
