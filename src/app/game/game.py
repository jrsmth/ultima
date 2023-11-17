import random
from flask import render_template, url_for, redirect, Blueprint
from src.app.model.board.threeboard import ThreeBoard
from src.app.model.mood import Mood
from src.app.model.status import Status
from src.version.version import __version__


# Game Logic
def construct_blueprint(redis, messages):
    game_page = Blueprint('game_page', __name__)

    @game_page.route("/game/<game_id>/<user_id>")
    def game(game_id, user_id):
        player_one_active = False
        player_two_active = False
        notification_active = False
        game_complete = False
        notification_header = ""
        notification_message = ""
        notification_icon = ""
        notification_mood = Mood.NEUTRAL.value

        if redis.get("whoseTurn") == 'player1':
            player_one_active = True
        else:
            player_two_active = True

        game_mode = redis.get("gameMode")
        board = redis.get_complex("board")
        game_state = get_game_state(redis, board)

        print(game_state)
        print("user id")
        print(user_id)
        print(redis.get("player1"))
        print(redis.get("player2"))
        if game_state != Status.IN_PROGRESS:
            notification_active = True
            game_complete = True

            if game_state == Status.DRAW:
                notification_header = messages.load("game.end.draw.header")
                notification_message = messages.load("game.end.draw.1.message")
                notification_icon = messages.load("game.end.draw.icon")

            elif game_state == Status.PLAYER_ONE_WINS:
                if redis.get("player1") == user_id:
                    notification_header = messages.load_with_params("game.end.win.header", [redis.get("player1")])
                    notification_icon = messages.load("game.end.win.icon")
                    notification_message = messages.load("game.end.win.1.message")
                    notification_mood = Mood.HAPPY.value
                else:
                    notification_header = messages.load_with_params("game.end.lose.header", [redis.get("player2")])
                    notification_icon = messages.load("game.end.lose.icon")
                    notification_message = messages.load("game.end.lose.3.message")
                    notification_mood = Mood.SAD.value

            elif game_state == Status.PLAYER_TWO_WINS:
                if redis.get("player2") == user_id:
                    notification_header = messages.load_with_params("game.end.win.header", [redis.get("player2")])
                    notification_icon = messages.load("game.end.win.icon")
                    notification_message = messages.load("game.end.win.3.message")
                    notification_mood = Mood.HAPPY.value
                else:
                    notification_header = messages.load_with_params("game.end.lose.header", [redis.get("player1")])
                    notification_icon = messages.load("game.end.lose.icon")
                    notification_message = messages.load("game.end.lose.1.message")
                    notification_mood = Mood.SAD.value

        return render_template(
            "game.html",
            board=board,
            playableSquare=redis.get("playableSquare"),
            innerStates=redis.get_complex("innerStates"),
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
            gameId=game_id,
            gameMode=game_mode,
            playerMode=redis.get("playerMode"),
            notificationActive=notification_active,
            notificationHeader=notification_header,
            notificationMessage=notification_message,
            notificationIcon=notification_icon,
            notificationMood=notification_mood,
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
    def place_standard_move(game_id, user_id, square):
        # Set player's move
        symbol = redis.get(user_id)
        board_list = redis.get_complex("board")
        board_list[int(square)] = int(symbol)
        redis.set_complex("board", board_list)

        # Switch player turn
        if redis.get("whoseTurn") == 'player1':
            # TODO :: I need to test the game state here to prevent the Computer from placing after I win...
            redis.set("whoseTurn", "player2")
            if redis.get("playerMode") == "SINGLE":
                print("[SINGLE] Computer is placing move")
                # Of the remaining available squares, select one at random
                current_board = redis.get_complex("board")
                print("[SINGLE] Board: " + str(current_board))
                available_squares = [index for index, square in enumerate(current_board) if square == 0]
                print("[SINGLE] Available: " + str(available_squares))
                if available_squares:
                    place_standard_move(game_id, "Computer", random.choice(available_squares))

        elif redis.get("whoseTurn") == 'player2':
            redis.set("whoseTurn", "player1")

        return redirect(url_for("game_page.game", game_id=game_id, user_id=user_id))

    @game_page.route("/game/<game_id>/place-move/<user_id>/<outer_square>/<inner_square>")
    def place_ultimate_move(game_id, user_id, outer_square, inner_square):
        # Set player's move
        symbol = redis.get(user_id)
        board = redis.get_complex("board")
        board[int(outer_square)][int(inner_square)] = int(symbol)
        redis.set_complex("board", board)

        print("[place_ultimate_move] outer_square: " + outer_square)
        print("[place_ultimate_move] inner_square: " + inner_square)
        print(board)

        # Set next playable outer square
        if get_game_state(redis, board[int(inner_square)]) != Status.IN_PROGRESS:
            redis.set("playableSquare", "-1")  # -1 is all squares...
        else:
            redis.set("playableSquare", inner_square)

        print("[place_ultimate_move] playableSquare: " + redis.get("playableSquare"))

        # Switch player turn
        if redis.get("whoseTurn") == 'player1':
            redis.set("whoseTurn", "player2")
        elif redis.get("whoseTurn") == 'player2':
            redis.set("whoseTurn", "player1")

        return redirect(url_for("game_page.game", game_id=game_id, user_id=user_id))

    # Closing return
    return game_page


def get_game_state(redis, board):
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

    if isinstance(board[0], list):
        print("[get_game_state] board[0]: " + str(board[0]))
        inner_states = []
        for outer_square in board:
            inner_state = get_game_state(redis, outer_square)
            inner_states.append(inner_state.value)
            print("[get_game_state] inner_states: " + str(inner_states))
            if len(inner_states) == 9 and inner_states.count(1) == 0:
                return Status.DRAW
        redis.set_complex("innerStates", inner_states)
        return get_game_state(redis, create_false_board(inner_states))

    if board.count(0) == 0:
        return Status.DRAW
        # FixMe :: this check needs to happen after test each player has won...
        # Note :: There is probs a clean way to split this up so that you don't iterate when not nec...

    print("count: " + str(board.count(1)))
    if (board.count(1)) >= 3:
        player_moves = get_player_moves(1, board)
        print(player_moves)
        for combo in winning_combos:
            print(combo)
            if set(combo).issubset(set(player_moves)):
                return Status.PLAYER_ONE_WINS

    if (board.count(2)) >= 3:
        player_moves = get_player_moves(2, board)
        for combo in winning_combos:
            if set(combo).issubset(set(player_moves)):
                return Status.PLAYER_TWO_WINS

    return Status.IN_PROGRESS


def get_player_moves(player, board):
    player_moves = []
    for index in range(len(board)):
        if board[index] == player:
            player_moves.append(index)

    return player_moves


def convert_states_to_symbols(state):
    if state == 1: return 0
    if state == 2: return 0
    if state == 3: return 1
    if state == 4: return 2


def create_false_board(states):
    board = ThreeBoard()
    board.top_lhs = convert_states_to_symbols(states[0])
    board.top_mid = convert_states_to_symbols(states[1])
    board.top_rhs = convert_states_to_symbols(states[2])
    board.mid_lhs = convert_states_to_symbols(states[3])
    board.mid_mid = convert_states_to_symbols(states[4])
    board.mid_rhs = convert_states_to_symbols(states[5])
    board.bot_lhs = convert_states_to_symbols(states[6])
    board.bot_mid = convert_states_to_symbols(states[7])
    board.bot_rhs = convert_states_to_symbols(states[8])

    print("[create_false_board] board: " + str(board.list()))
    return board.list()
