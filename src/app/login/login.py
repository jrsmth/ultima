from flask import redirect, url_for, render_template, Blueprint, request

from src.app.model.board.nineboard import NineBoard
from src.app.model.board.threeboard import ThreeBoard


# Login Logic
def construct_blueprint(redis, messages):
    login_page = Blueprint('login_page', __name__)

    @login_page.route('/', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == "POST":
            print(request.form["name"])  # log me
            print(request.form["gameId"])
            print(request.form["gameMode"])

            game_mode = request.form["gameMode"]
            if game_mode == "STANDARD":
                redis.set("gameMode", game_mode)
                board = ThreeBoard()
                board_list = ThreeBoard.list(board)
                # second index is the state: 0 for empty, 1 for cross, 2 for circle
                redis.set_complex("board", board_list)

            elif game_mode == "ULTIMATE":
                redis.set("gameMode", game_mode)
                board = NineBoard()
                board_list = NineBoard.list(board)
                # second index is the state: 0 for empty, 1 for cross, 2 for circle
                redis.set_complex("board", board_list)

            else:
                print("Game Mode already set [" + redis.get("gameMode") + "]")  # TODO :: err handle

            print(redis.get_complex("board"))

            # TODO :: set redis obj as dict { $game_id: [player1: "", player2: ""] }
            if request.form["gameId"] == "":
                redis.set("player1", request.form["name"])
                redis.set("player2", "")
                redis.set(request.form["name"], "1")  # For now, set first player to cross
                redis.set("whoseTurn", "player1")
                return redirect(url_for("game_page.game", game_id=generate_game_id(), user_id=request.form["name"]))

            elif has_valid_game_id(request.form["gameId"]):
                redis.set("player2", request.form["name"])
                redis.set(request.form["name"], "2")  # For now, set first player to circle
                return redirect(url_for("game_page.game", game_id=request.form["gameId"], user_id=request.form["name"]))

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
    return "ab12-3cd4-e5f6-78gh"
