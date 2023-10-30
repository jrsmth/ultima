import os
import sys
from flask import Flask, render_template, redirect, url_for, request
from flask_redis import FlaskRedis

from config import Config, DevConfig, ProductionConfig
from model.status import Status
from version.version import __version__
from pyjavaproperties import Properties

app = Flask(
    __name__,
    template_folder=os.path.abspath('./resources/templates'),
    static_folder='resources/static'
)
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

redis_client = FlaskRedis(app)
# TODO :: switch to snake_case?

messages = Properties()
messages.load(open('resources/message.properties'))


@app.route("/game/<id>/<userId>")
def game(id, userId):
    print("hit")
    player_one_active = False
    player_two_active = False
    notification_active = False
    game_complete = False
    notification_message = ""

    if get("whoseTurn") == 'player1':
        player_one_active = True
    else:
        player_two_active = True

    game_state = get_game_state()
    print(game_state)
    if game_state != Status.IN_PROGRESS:
        notification_active = True
        game_complete = True
        if game_state == Status.DRAW:
            notification_message = messages["end-game.draw"]
        elif game_state == Status.PLAYER_ONE_WINS:
            notification_message = messages["end-game.player-one"]
        elif game_state == Status.PLAYER_TWO_WINS:
            notification_message = messages["end-game.player-two"]

    return render_template(
        "game.html",
        one=get("1"),
        two=get("2"),
        three=get("3"),
        four=get("4"),
        five=get("5"),
        six=get("6"),
        seven=get("7"),
        eight=get("8"),
        nine=get("9"),
        gameComplete=game_complete,
        notificationActive=notification_active,
        notificationMessage=notification_message,
        player1=get("player1"),
        player2=get("player2"),
        playerOneActive=player_one_active,
        playerTwoActive=player_two_active,
        thisUserId=userId,
        thisUserSymbol=get(userId),
        version=__version__,
        whoseTurn=get("whoseTurn")
    )


@app.route("/game/<id>/place-move/<user_id>/<square>")
def place_move(id, user_id, square):
    print(id)
    print(user_id)
    print(square)

    symbol = get(user_id)
    redis_client.set(square, symbol)

    # Switch user
    if get("whoseTurn") == 'player1':
        redis_client.set("whoseTurn", "player2")
    elif get("whoseTurn") == 'player2':
        redis_client.set("whoseTurn", "player1")

    return redirect(url_for("game", id=id, userId=user_id))


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
        # second index is the state: 0 for empty, 1 for cross, 2 for circle
        redis_client.set("1", 0)
        redis_client.set("2", 0)
        redis_client.set("3", 0)
        redis_client.set("4", 0)
        redis_client.set("5", 0)
        redis_client.set("6", 0)
        redis_client.set("7", 0)
        redis_client.set("8", 0)
        redis_client.set("9", 0)


    # TODO :: set redis obj as dict { $game_id: [player1: "", player2: ""] }
        if request.form["gameId"] == "":
            redis_client.set("player1", request.form["name"])
            redis_client.set("player2", "")
            redis_client.set(request.form["name"], "1") # For now, set first player to cross
            redis_client.set("whoseTurn", "player1")
            return redirect(url_for("game", id=generateGameId(), userId=request.form["name"]))

        elif isValidGameId(request.form["gameId"]):
            redis_client.set("player2", request.form["name"])
            redis_client.set(request.form["name"], "2") # For now, set first player to circle
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


def get(key):
    return redis_client.get(key).decode('utf-8')


def get_game_state():
    board = {
        "1": get("1"), "2": get("2"), "3": get("3"),
        "4": get("4"), "5": get("5"), "6": get("6"),
        "7": get("7"), "8": get("8"), "9": get("9"),
    }

    winning_combos = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
        [1, 5, 9],
        [3, 5, 7],
    ]

    if list(board.values()).count("0") == 0:
        return Status.DRAW

    print("count: " + str(list(board.values()).count("1")))
    if (list(board.values()).count("1")) >= 3:
        player_moves = get_player_moves("1", board)
        print(player_moves)
        for combo in winning_combos:
            print(combo)
            if set(combo).issubset(set(player_moves)):
                return Status.PLAYER_ONE_WINS

    if (list(board.values()).count("2")) >= 3:
        player_moves = get_player_moves("2", board)
        for combo in winning_combos:
            if set(combo).issubset(set(player_moves)):
                return Status.PLAYER_TWO_WINS

    return Status.IN_PROGRESS

def get_player_moves(player, board):
    return [int(k) for k, v in board.items() if v == player]


if __name__ == "__main__":
    app.run()
