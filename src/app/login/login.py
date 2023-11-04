from flask import redirect, url_for, render_template, Blueprint, request


def construct_blueprint(client, messages):
    login_page = Blueprint('login_page', __name__)

    @login_page.route('/', methods=['GET', 'POST'])
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
            client.set("1", 0)
            client.set("2", 0)
            client.set("3", 0)
            client.set("4", 0)
            client.set("5", 0)
            client.set("6", 0)
            client.set("7", 0)
            client.set("8", 0)
            client.set("9", 0)

            # TODO :: set redis obj as dict { $game_id: [player1: "", player2: ""] }
            if request.form["gameId"] == "":
                client.set("player1", request.form["name"])
                client.set("player2", "")
                client.set(request.form["name"], "1")  # For now, set first player to cross
                client.set("whoseTurn", "player1")
                return redirect(url_for("game_page.game", game_id=generate_game_id(), user_id=request.form["name"]))

            elif has_valid_game_id(request.form["gameId"]):
                client.set("player2", request.form["name"])
                client.set(request.form["name"], "2")  # For now, set first player to circle
                return redirect(url_for("game_page.game", game_id=request.form["gameId"], user_id=request.form["name"]))

            else:
                error = "Invalid Game Id :: Please try again or leave blank to start a new game"

        return render_template("login.html", error=error)

    return login_page


def has_valid_game_id(id):
    if id != "-1":  # Does game id already exist?
        return True
    else:
        return False


def generate_game_id():
    return "ab12-3cd4-e5f6-78gh"
