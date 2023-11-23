import shortuuid
from flask import redirect, url_for, render_template, Blueprint, request

from src.app.model.board.nineboard import NineBoard
from src.app.model.board.threeboard import ThreeBoard
from src.app.model.game import Game
from src.app.model.mode.gamemode import GameMode


# Login Logic
def construct_blueprint(messages, socket, redis):
    login_page = Blueprint('login_page', __name__)

    @login_page.route('/', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == "POST":
            print(request.form["name"])  # log me
            print(request.form["gameId"])
            print(request.form["gameMode"])
            print(request.form["playerMode"])
            print(bool(request.form["restart"]))
            game_id = request.form["gameId"]
            user_id = request.form["name"]
            game_mode = request.form["gameMode"]

            if bool(request.form["restart"]):
                redis.set("whoseTurn", "player1")
                return redirect(url_for("game_page.game", game_id=request.form["gameId"], user_id=request.form["name"]))

            # Set up player one - Question :: extract?
            if request.form["gameId"] == "":
                game_id = generate_game_id()
                game = Game()
                game.game_id = game_id
                game.game_mode = game_mode
                game.player_one.name = request.form["name"]
                game.board = generate_board(game_mode)

                if redis.get("playerMode") == "SINGLE":
                    game.player_two.name = "Computer"

                print("[login] Setting game object: " + game.to_string())
                redis.set_complex(game_id, game)
                return redirect(url_for("game_page.game", game_id=game_id, user_id=user_id))

            elif has_valid_game_id(request.form["gameId"]):
                print("Testing playMode [" + request.form["playerMode"] + "]")
                if redis.get("playerMode") == "SINGLE":
                    print("Player Mode set to [SINGLE] for game id [" + redis.get("playerMode") + "]")
                    error = messages.load("login.error.single-player-only")

                else:
                    game = redis.get_complex(game_id)
                    game['player_two']['name'] = request.form["name"]  # TODO :: marshal dict into Game obj
                    print("[login] Setting game object: " + str(game))
                    # print("[login] Setting game object: " + game.to_string())
                    redis.set_complex(game_id, game)
                    return redirect(url_for("game_page.game", game_id=game_id, user_id=user_id))

            else:
                error = messages.load("login.error.invalid-game-id")

        return render_template("login.html", error=error)

    # Closing return
    return login_page


def has_valid_game_id(game_id):
    if game_id != "-1":  # Does game id already exist?
        return True
    else:
        return False


def generate_game_id():
    return shortuuid.uuid()[:12]
    # return "ab12-3cd4-e5f6-78gh"


def generate_board(game_mode):
    if game_mode == GameMode.STANDARD.value:
        return ThreeBoard().list()
    elif game_mode == GameMode.ULTIMATE.value:
        return NineBoard().list()

    else:
        print("Game Mode already set [" + game_mode + "]")  # TODO :: err handle
