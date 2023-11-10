from flask import redirect, url_for, render_template, Blueprint, request

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
            board = ThreeBoard()
            board_list = ThreeBoard.list(board)
            # first index is squareNo
            # second index is the state: 0 for empty, 1 for cross, 2 for circle
            redis.set("0", board_list[0])
            redis.set("1", board_list[1])
            redis.set("2", board_list[2])
            redis.set("3", board_list[3])
            redis.set("4", board_list[4])
            redis.set("5", board_list[5])
            redis.set("6", board_list[6])
            redis.set("7", board_list[7])
            redis.set("8", board_list[8])

            game_mode = request.form["gameMode"]
            if game_mode != "":
                redis.set("gameMode", game_mode)
            else:
                print("Game Mode already set [" + redis.get("gameMode") + "]");  # TODO :: err handle

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

    return login_page


def has_valid_game_id(game_id):
    if game_id != "-1":  # Does game id already exist?
        return True
    else:
        return False


def generate_game_id():
    return "ab12-3cd4-e5f6-78gh"
