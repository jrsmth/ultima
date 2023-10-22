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


@app.route("/game/<id>/<userId>")
def game(id, userId):
    print("hit")
    return render_template(
        "game.html",
        one=redis_client.get("1"),
        two=redis_client.get("2"),
        three=redis_client.get("3"),
        four=redis_client.get("4"),
        five=redis_client.get("5"),
        six=redis_client.get("6"),
        seven=redis_client.get("7"),
        eight=redis_client.get("8"),
        nine=redis_client.get("9"),
        player1=redis_client.get("player1"),
        player2=redis_client.get("player2"),
        thisUserId=userId,
        thisUserSymbol=redis_client.get(userId),
        version=__version__
    )

@app.route("/game/<id>/place-move/<userId>/<square>")
def placeMove(id, userId, square):
    print(id)
    print(userId)
    print(square)

    redis_client.set(square, "1")
    return redirect(url_for("game", id=id, userId=userId))

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        print(request.form["name"])  # log me
        print(request.form["gameId"])
        board = [(1, 0), (2, 0), (3, 0),
                 (4, 0), (5, 0), (6, 0),
                 (7, 0), (8, 0), (9, 0)]
        # first index is squareNo
        # second index is the state: 0 for empty, 1 for circle, 2 for cross
        redis_client.set("1", 0)
        redis_client.set("2", 1)
        redis_client.set("3", 0)
        redis_client.set("4", 2)
        redis_client.set("5", 0)
        redis_client.set("6", 2)
        redis_client.set("7", 0)
        redis_client.set("8", 0)
        redis_client.set("9", 0)


    # TODO :: set redis obj as dict { $game_id: [player1: "", player2: ""] }
        if request.form["gameId"] == "":
            redis_client.set("player1", request.form["name"])
            redis_client.set(request.form["name"], "1") # For now, set this player's symbol to circle
            return redirect(url_for("game", id=generateGameId(), userId=request.form["name"]))

        elif isValidGameId(request.form["gameId"]):
            redis_client.set("player2", request.form["name"])
            return redirect(url_for("game", id=request.form["gameId"], userId=request.form["name"]))

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
