import os
import sys
from flask import Flask, render_template, redirect, url_for, request
from flask_redis import FlaskRedis
from config import Config, ProductionConfig
from version.version import __version__

app = Flask(__name__)
env = os.environ.get("FLASK_ENV")

if not env:
    raise ValueError("Start-up failed: no environment specified!")
elif env == "local":
    app.config.from_object(Config())
    print("Starting app in [local] mode")
elif env == "prod":
    app.config.from_object(ProductionConfig())
    print("Starting app in [production] mode")

redis_client = FlaskRedis(app)
# TODO :: switch to snake_case?


@app.route("/game/<id>")
def game(id):
    return render_template("game.html", version=__version__, player1=redis_client.get("player1"), player2=redis_client.get("player2"))


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        print(request.form["name"])  # log me
        print(request.form["gameId"])

        # TODO :: set redis obj as dict { $game_id: [player1: "", player2: ""] }
        if request.form["gameId"] == "":
            redis_client.set("player1", request.form["name"])
            return redirect(url_for("game", id=generateGameId()))

        elif isValidGameId(request.form["gameId"]):
            redis_client.set("player2", request.form["name"])
            return redirect(url_for("game", id=request.form["gameId"]))

        else:
            error = "Invalid Game Id :: Please try again or leave blank to start a new game"

    return render_template("login.html", error=error)


@app.route("/game/<id>/clear")
def clear_game():
    return ""  # TODO :: clear the game state for given id


def isValidGameId(id):
    if id != "-1":  # Does game id already exist?
        return True
    else:
        return False


def generateGameId():
    return "ab12-3cd4-e5f6-78gh"


if __name__ == "__main__":
    app.run()
