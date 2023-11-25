import json
import random

from flask import render_template, url_for, redirect, Blueprint, Response

from src.app.model.board.threeboard import ThreeBoard
from src.app.model.combos import get_wins
from src.app.model.game import generate_board
from src.app.model.mode.gamemode import GameMode
from src.app.model.mode.playermode import PlayerMode
from src.app.model.mood import Mood
from src.app.model.notification import Notification
from src.app.model.status import Status
from src.version.version import __version__


# Game Logic
def construct_blueprint(messages, socket, redis):
    game_page = Blueprint('game_page', __name__)

    @game_page.route("/game/<game_id>/<user_id>")
    def game(game_id, user_id):
        update_game_state(game_id, user_id + ' has joined the game')
        check_status(game_id)

        return render_template("game.html", gameId=game_id, userId=user_id, version=__version__)

    @socket.on('restart')
    def restart(message):
        game_id = message['gameId']
        user_id = message['userId']
        game_state = redis.get_complex(game_id)
        print(f"[restart] Received restart from [{ user_id }] for { game_id }")

        game_state["board"] = generate_board(game_state["game_mode"])
        game_state["complete"] = False
        game_state["player_one"]["notification"] = Notification()
        game_state["player_two"]["notification"] = Notification()

        redis.set_complex(game_id, game_state)
        update_game_state(game_id, user_id + ' has restarted the game')

    @game_page.route("/game/<game_id>/place-move/<user_id>/<square>")
    def place_standard_move(game_id, user_id, square):
        print("[place_standard_move] [" + game_id + "] [" + user_id + "] Placing square with index: " + square)

        # Set player's move
        current_state = redis.get_complex(game_id)  # Question :: marshal into obj?
        board = current_state["board"]
        print("[place_standard_move] Board retrieved: " + str(board))

        players = [current_state["player_one"], current_state["player_two"]]
        user_symbol = [player for player in players if player["name"] == user_id][0]["symbol"]
        # Could be more elegant ^
        board[int(square)] = user_symbol
        current_state["board"] = board

        # Switch player turn
        if current_state["player_turn"] == 1:
            # TODO :: I need to test the game state here to prevent the Computer from placing after I win...
            current_state["player_turn"] = 2
            if redis.get("playerMode") == PlayerMode.SINGLE.value:
                available_squares = [index for index, square in enumerate(current_state["board"]) if square == 0]
                print("[place_standard_move] [single] Available squares: " + str(available_squares))
                if available_squares:
                    print("[place_standard_move] [single] Computer is placing move in random available square")
                    place_standard_move(game_id, "Computer", random.choice(available_squares))

        elif current_state["player_turn"] == 2:
            current_state["player_turn"] = 1

        redis.set_complex(game_id, current_state)
        check_status(game_id)

        update_game_state(game_id, user_id + ' has placed move on square ' + square)

        return Response(status=204)

    @game_page.route("/game/<game_id>/place-move/<user_id>/<outer_square>/<inner_square>")
    def place_ultimate_move(game_id, user_id, outer_square, inner_square):
        # Set player's move
        symbol = redis.get(user_id)
        board = redis.get_complex("board")
        board[int(outer_square)][int(inner_square)] = int(symbol)
        redis.set_complex("board", board)

        print("[place_ultimate_move] outer_square: " + str(outer_square))
        print("[place_ultimate_move] inner_square: " + str(inner_square))
        print(board)

        # Set next playable outer square
        if get_game_state(redis, board[int(inner_square)]) != Status.IN_PROGRESS:
            redis.set("playableSquare", "-1")  # -1 is all squares...
        else:
            redis.set("playableSquare", inner_square)

        print("[place_ultimate_move] playableSquare: " + redis.get("playableSquare"))

        # Switch player turn
        if redis.get("whoseTurn") == 'player1':
            # TODO :: I need to test the game state here to prevent the Computer from placing after I win...
            redis.set("whoseTurn", "player2")
            if redis.get("playerMode") == "SINGLE":
                print("[SINGLE][ULTIMATE] Computer is placing move")
                # Of the remaining available squares, select one at random

                # Prevent computer from placing in an already completed outer square
                chosen_outer_square = int(inner_square)
                if redis.get("playableSquare") == "-1":
                    inner_states = redis.get_complex("innerStates")
                    available_outers = [index for index, state in enumerate(inner_states) if state == 1]
                    chosen_outer_square = random.choice(available_outers)

                current_board = redis.get_complex("board")[chosen_outer_square]
                print("[SINGLE][ULTIMATE] Board: " + str(current_board))
                available_squares = [index for index, square in enumerate(current_board) if square == 0]
                print("[SINGLE][ULTIMATE] Available: " + str(available_squares))
                if available_squares:
                    place_ultimate_move(game_id, "Computer", chosen_outer_square, random.choice(available_squares))

        elif redis.get("whoseTurn") == 'player2':
            redis.set("whoseTurn", "player1")

        return redirect(url_for("game_page.game", game_id=game_id, user_id=user_id))

    @game_page.route('/game/state/<game_id>')
    def get_game_state(game_id):
        game_state = redis.get_complex(game_id)
        print('[retrieve_game_state] Retrieving game state: ' + str(game_state))
        return Response(status=200, content_type='application/json', response=json.dumps(game_state))
        # Question :: Custom Response class?

    def update_game_state(game_id, description):
        print('[update_game_state] Game state update: ' + description)
        print('[update_game_state] Game state updated for game id: ' + game_id)
        socket.emit('update_game_state', redis.get_complex(game_id))

    def check_status(game_id):
        state = redis.get_complex(game_id)
        print("[check_status] Checking status for game with state: " + str(state))
        status = calculate_game_status(state)
        print("[check_status] Status determined to be: " + str(status))

        if status != Status.IN_PROGRESS:
            state["player_one"]["notification"] = build_notification(state, messages, status, 1)
            state["player_two"]["notification"] = build_notification(state, messages, status, 2)
            state["complete"] = True
            redis.set_complex(game_id, state)

    def calculate_game_status(state):
        print("[calculate_game_status] Calculating status for game with mode: " + state["game_mode"])
        if state["game_mode"] == GameMode.ULTIMATE.value:
            return calculate_ultimate_status(state)
        if state["board"].count(0) == 0:
            return Status.DRAW
        elif has_player_won(state["board"], 1):
            return Status.PLAYER_ONE_WINS
        elif has_player_won(state["board"], 2):
            return Status.PLAYER_TWO_WINS
        else:
            return Status.IN_PROGRESS

    def calculate_ultimate_status(state):
        board = state["board"]
        outer_states = []
        for outer_square in board:
            outer_state = calculate_game_status(outer_square)
            outer_states.append(outer_state.value)
            print("[calculate_ultimate_status] inner_states: " + str(outer_states))
            if len(outer_states) == 9 and outer_states.count(1) == 0:
                return Status.DRAW
        state["outer_states"] = outer_states
        redis.set_complex(state["game_id"], state)
        return calculate_game_status(create_false_board(outer_states))

    # Closing return
    return game_page


def has_player_won(board, player):
    if (board.count(player)) >= 3:
        player_moves = []

        for index in range(len(board)):
            if board[index] == player:
                player_moves.append(index)

        for combo in get_wins():
            if set(combo).issubset(set(player_moves)):
                return True

    return False


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


def build_notification(game_state, messages, game_status, player):
    print(f"[build_notification] Building notification for player [{player}] with status [{game_status}]")
    notification = Notification()
    notification.active = True

    if game_status == Status.DRAW:
        notification.title = messages.load("game.end.draw.header")
        notification.content = messages.load("game.end.draw.1.message")
        notification.icon = messages.load("game.end.draw.icon")
        return notification

    player_won = (game_status == Status.PLAYER_ONE_WINS and player == 1) or \
                 (game_status == Status.PLAYER_TWO_WINS and player == 2)

    player_name = game_state["player_" + ("one" if player == 1 else "two")]["name"]

    if player_won:
        notification.title = messages.load_with_params("game.end.win.header", [player_name])
        notification.content = messages.load("game.end.win.1.message")
        notification.icon = messages.load("game.end.win.icon")
        notification.mood = Mood.HAPPY.value
    else:
        notification.title = messages.load_with_params("game.end.lose.header", [player_name])
        notification.content = messages.load("game.end.lose.1.message")
        notification.icon = messages.load("game.end.lose.icon")
        notification.mood = Mood.SAD.value

    # TODO :: implement random message selection
    return notification
