from flask import render_template, url_for, redirect, Blueprint
from src.app.model.status import Status
from src.version.version import __version__


# # # # # # # # # # # # # # # #
# Game Routes
# # # # # # # # # # # # # # # #
def construct_blueprint(redis, messages):
    game_page = Blueprint('game_page', __name__)

    @game_page.route("/game/<game_id>/<user_id>")
    def game(game_id, user_id):
        player_one_active = False
        player_two_active = False
        notification_active = False
        game_complete = False
        notification_message = ""

        if redis.get("whoseTurn") == 'player1':
            player_one_active = True
        else:
            player_two_active = True

        game_state = get_game_state(redis)
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
            zero=redis.get("0"),
            one=redis.get("1"),
            two=redis.get("2"),
            three=redis.get("3"),
            four=redis.get("4"),
            five=redis.get("5"),
            six=redis.get("6"),
            seven=redis.get("7"),
            eight=redis.get("8"),
            gameComplete=game_complete,
            notificationActive=notification_active,
            notificationMessage=notification_message,
            player1=redis.get("player1"),
            player2=redis.get("player2"),
            playerOneActive=player_one_active,
            playerTwoActive=player_two_active,
            thisUserId=user_id,
            thisUserSymbol=redis.get(user_id),
            version=__version__,
            whoseTurn=redis.get("whoseTurn")
        )

    @game_page.route("/game/<game_id>/place-move/<user_id>/<square>")
    def place_move(game_id, user_id, square):
        # Set player's move
        symbol = redis.get(user_id)
        redis.set(square, symbol)

        # Switch player turn
        if redis.get("whoseTurn") == 'player1':
            redis.set("whoseTurn", "player2")
        elif redis.get("whoseTurn") == 'player2':
            redis.set("whoseTurn", "player1")

        return redirect(url_for("game_page.game", game_id=game_id, user_id=user_id))

    return game_page


def get_game_state(redis):
    board = {
        "0": redis.get("0"), "1": redis.get("1"), "2": redis.get("2"),
        "3": redis.get("3"), "4": redis.get("4"), "5": redis.get("5"),
        "6": redis.get("6"), "7": redis.get("7"), "8": redis.get("8"),
    }

    winning_combos = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    print(board)

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
