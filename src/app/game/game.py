from flask import render_template, url_for, redirect, Blueprint
from src.app.model.status import Status
from src.app.util.redis import get
from src.version.version import __version__


# # # # # # # # # # # # # # # #
# Game Routes
# # # # # # # # # # # # # # # #
def construct_blueprint(client, messages):
    game_page = Blueprint('game_page', __name__)

    @game_page.route("/game/<game_id>/<user_id>")
    def game(game_id, user_id):
        player_one_active = False
        player_two_active = False
        notification_active = False
        game_complete = False
        notification_message = ""

        if get(client, "whoseTurn") == 'player1':
            player_one_active = True
        else:
            player_two_active = True

        game_state = get_game_state(client)
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
            one=get(client, "1"),
            two=get(client, "2"),
            three=get(client, "3"),
            four=get(client, "4"),
            five=get(client, "5"),
            six=get(client, "6"),
            seven=get(client, "7"),
            eight=get(client, "8"),
            nine=get(client, "9"),
            gameComplete=game_complete,
            notificationActive=notification_active,
            notificationMessage=notification_message,
            player1=get(client, "player1"),
            player2=get(client, "player2"),
            playerOneActive=player_one_active,
            playerTwoActive=player_two_active,
            thisUserId=user_id,
            thisUserSymbol=get(client, user_id),
            version=__version__,
            whoseTurn=get(client, "whoseTurn")
        )

    @game_page.route("/game/<game_id>/place-move/<user_id>/<square>")
    def place_move(game_id, user_id, square):
        # Set player's move
        symbol = get(client, user_id)
        client.set(square, symbol)

        # Switch player turn
        if get(client, "whoseTurn") == 'player1':
            client.set("whoseTurn", "player2")
        elif get(client, "whoseTurn") == 'player2':
            client.set("whoseTurn", "player1")

        return redirect(url_for("game", game_id=game_id, user_id=user_id))

    return game_page


def get_game_state(client):
    board = {
        "1": get(client, "1"), "2": get(client, "2"), "3": get(client, "3"),
        "4": get(client, "4"), "5": get(client, "5"), "6": get(client, "6"),
        "7": get(client, "7"), "8": get(client, "8"), "9": get(client, "9"),
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
