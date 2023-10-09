import sys
from flask import Flask, render_template, redirect, url_for, request
from flask_redis import FlaskRedis

app = Flask(__name__)
redis_client = FlaskRedis(app)
# TODO :: switch to snake_case?


@app.route("/game/<id>")
def game(id):
    return render_template("game.html", player1=redis_client.get("player1"), player2=redis_client.get("player2"))


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


if __name__ == "__main__":
    app.run()


def isValidGameId(id):
    if id != "-1":  # Does game id already exist?
        return True
    else:
        return False

def generateGameId():
    return "ab12-3cd4-e5f6-78gh"
