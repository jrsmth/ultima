import json
import random
import time

from flask import render_template, Blueprint, Response, current_app
from src.app.model.board.board import map_to_symbol
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
def construct_blueprint(messages, redis, socket):
    game_page = Blueprint('game_page', __name__)

    @game_page.route("/game/<game_id>/<user_id>")
    def game(game_id, user_id):
        app_url = current_app.config["APP_URL"]
        update_game_state(game_id, user_id + ' has joined the game')
        check_status(game_id)

        return render_template("game.html",
                               appUrl=app_url, messages=messages.load_all(), version=__version__,
                               gameId=game_id, userId=user_id)

    @socket.on('restart')
    def restart(message):
        game_id = message['gameId']
        user_id = message['userId']
        game_state = redis.get_complex(game_id)
        print(f"[restart] Received restart from [{user_id}] for {game_id}")

        game_state["complete"] = False
        game_state["player_one"]["notification"] = Notification()
        game_state["player_two"]["notification"] = Notification()
        game_state["board"] = generate_board(game_state["game_mode"])
        game_state["playable_square"] = -1
        game_state["outer_states"] = [  # List of states for each outer square -> # Question :: better way?
            Status.IN_PROGRESS.value, Status.IN_PROGRESS.value, Status.IN_PROGRESS.value,
            Status.IN_PROGRESS.value, Status.IN_PROGRESS.value, Status.IN_PROGRESS.value,
            Status.IN_PROGRESS.value, Status.IN_PROGRESS.value, Status.IN_PROGRESS.value
        ]

        if game_state["player_mode"] == PlayerMode.SINGLE.value:
            game_state["player_turn"] = 1

        redis.set_complex(game_id, game_state)
        update_game_state(game_id, user_id + ' has restarted the game')

    @game_page.route("/game/<game_id>/place-move/<user_id>/<square>")
    def place_standard_move(game_id, user_id, square):
        print("[place_standard_move] [" + game_id + "] [" + user_id + "] Placing square with index: " + square)

        # Set player's move
        index_tuple = (int(square))
        current_state = set_player_move(game_id, user_id, index_tuple)

        # Switch player turn
        if current_state["player_turn"] == 1:
            current_state["player_turn"] = 2
            redis.set_complex(game_id, current_state)
            if check_status(game_id) != Status.IN_PROGRESS:
                update_game_state(game_id, user_id + ' has placed move on square ' + square)
                return Response(status=204)

            # Place Computer move [single mode]
            elif current_state["player_mode"] == PlayerMode.SINGLE.value:
                # Update user first then simulate computer thinking time
                update_game_state(game_id, "Computer is now placing move")  # Note: sub-par logs (b4 'user has placed')
                simulate_computer_think_time()
                set_standard_computer_move(game_id, current_state["board"])

        elif current_state["player_turn"] == 2:
            current_state["player_turn"] = 1
            redis.set_complex(game_id, current_state)

        check_status(game_id)
        update_game_state(game_id, user_id + ' has placed move on square ' + square)
        return Response(status=204)

    @game_page.route("/game/<game_id>/place-move/<user_id>/<outer_square>/<inner_square>")
    def place_ultimate_move(game_id, user_id, outer_square, inner_square):
        outer_index = int(outer_square)
        inner_index = int(inner_square)
        print(f"[place_ultimate_move] [{game_id}] [{user_id}] Placing move with on [{outer_square}] [{inner_square}]")

        # Set player's move
        index_tuple = (outer_index, inner_index)
        current_state = set_player_move(game_id, user_id, index_tuple)

        # Set next playable outer square
        status = calculate_game_status(current_state, current_state["board"][inner_index])
        if status != Status.IN_PROGRESS:
            current_state["playable_square"] = -1
        else:
            current_state["playable_square"] = inner_index
        print("[place_ultimate_move] Next playable square set to: " + str(current_state["playable_square"]))

        # Switch player turn
        if current_state["player_turn"] == 1:
            current_state["player_turn"] = 2
            redis.set_complex(game_id, current_state)

            if check_status(game_id) != Status.IN_PROGRESS:
                update_game_state(game_id, user_id + ' has placed on [' + outer_square + "] [" + inner_square + "]")
                return Response(status=204)

            # Place Computer move [single mode]
            elif current_state["player_mode"] == PlayerMode.SINGLE.value:
                # Update user first then simulate computer thinking time
                update_game_state(game_id, "Computer is now placing move")  # Note: sub-par logs (b4 'user has placed')
                simulate_computer_think_time()
                set_ultimate_computer_move(game_id, inner_index)

        elif current_state["player_turn"] == 2:
            current_state["player_turn"] = 1
            redis.set_complex(game_id, current_state)

        check_status(game_id)
        update_game_state(game_id, user_id + ' has placed on [' + str(outer_square) + "] [" + str(inner_square) + "]")
        return Response(status=204)

    @game_page.route('/game/state/<game_id>')
    def get_game_state(game_id):
        game_state = redis.get_complex(game_id)
        print('[retrieve_game_state] Retrieving game state: ' + str(game_state))
        return Response(status=200, content_type='application/json', response=json.dumps(game_state))

    def update_game_state(game_id, description):
        print('[update_game_state] Game state update: ' + description)
        print('[update_game_state] Game state updated for game id: ' + game_id)
        socket.emit('update_game_state', redis.get_complex(game_id), to=game_id)

    def check_status(game_id):
        state = redis.get_complex(game_id)
        print("[check_status] Checking status for game with state: " + str(state))
        status = calculate_game_status(state, state["board"])
        print("[check_status] Status determined to be: " + str(status))

        if status != Status.IN_PROGRESS:
            state["player_one"]["notification"] = build_notification(state, messages, status, 1)
            state["player_two"]["notification"] = build_notification(state, messages, status, 2)
            state["complete"] = True
            redis.set_complex(game_id, state)
        return status

    def calculate_game_status(state, test_board):
        print("[calculate_game_status] Calculating status for game with mode: " + state["game_mode"])
        print("[calculate_game_status] Calculating status for test board: " + str(test_board))
        if isinstance(test_board[0], list):
            return calculate_ultimate_status(state, test_board)
        if has_player_won(test_board, 1):
            return Status.PLAYER_ONE_WINS
        elif has_player_won(test_board, 2):
            return Status.PLAYER_TWO_WINS
        if test_board.count(0) == 0:
            return Status.DRAW
        else:
            return Status.IN_PROGRESS

    def calculate_ultimate_status(state, board):
        print(f"[calculate_ultimate_status] Calculating status for board: {board}")
        outer_states = []
        for outer_square in board:
            outer_state = calculate_game_status(state, outer_square)
            outer_states.append(outer_state.value)
            print("[calculate_ultimate_status] outer_states: " + str(outer_states))
            if len(outer_states) == 9 and outer_states.count(1) == 0:
                status = calculate_game_status(state, create_false_board(outer_states))
                print("[calculate_ultimate_status] does last move clinch the winner? -> status: " + str(status))
                return Status.DRAW if status == Status.IN_PROGRESS else status
        state["outer_states"] = outer_states
        redis.set_complex(state["game_id"], state)
        return calculate_game_status(state, create_false_board(outer_states))

    def set_player_move(game_id, user_id, index_tuple):
        current_state = redis.get_complex(game_id)
        board = current_state["board"]
        print("[set_player_move] Board retrieved: " + str(board))

        players = [current_state["player_one"], current_state["player_two"]]
        user_symbol = [player for player in players if player["name"] == user_id][0]["symbol"]  # Could be more elegant

        if current_state["game_mode"] == GameMode.STANDARD.value:
            board[index_tuple] = user_symbol
        elif current_state["game_mode"] == GameMode.ULTIMATE.value:
            board[index_tuple[0]][index_tuple[1]] = user_symbol

        current_state["board"] = board
        return current_state

    def set_standard_computer_move(game_id, board):
        available_squares = [index for index, square in enumerate(board) if square == 0]
        print("[set_standard_computer_move] Available squares: " + str(available_squares))
        if available_squares:
            print("[set_standard_computer_move] Computer is placing move in random available square")
            place_standard_move(game_id, "Computer", str(random.choice(available_squares)))

    def set_ultimate_computer_move(game_id, inner_square):
        print("[set_ultimate_computer_move] Computer is placing move in a random available square")
        game_state = redis.get_complex(game_id)

        # Prevent computer from placing in an already completed outer square
        chosen_outer_square = inner_square
        if game_state["playable_square"] == -1:
            available_outers = [index for index, state in enumerate(game_state["outer_states"]) if state == 1]
            chosen_outer_square = random.choice(available_outers)

        current_board = game_state["board"][chosen_outer_square]
        print("[set_ultimate_computer_move] Board: " + str(current_board))
        available_squares = [index for index, square in enumerate(current_board) if square == 0]
        print("[set_ultimate_computer_move] Available: " + str(available_squares))
        if available_squares:
            place_ultimate_move(game_id, "Computer", chosen_outer_square, random.choice(available_squares))

    # Blueprint return
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


# In ULTIMATE mode, a 'False Board' is defined to be the 3x3 board of resolved outer squares
def create_false_board(states):  # Question :: does a more elegant way exist?
    board = ThreeBoard()
    board.top_lhs = map_to_symbol(states[0])
    board.top_mid = map_to_symbol(states[1])
    board.top_rhs = map_to_symbol(states[2])
    board.mid_lhs = map_to_symbol(states[3])
    board.mid_mid = map_to_symbol(states[4])
    board.mid_rhs = map_to_symbol(states[5])
    board.bot_lhs = map_to_symbol(states[6])
    board.bot_mid = map_to_symbol(states[7])
    board.bot_rhs = map_to_symbol(states[8])

    print("[create_false_board] board: " + str(board.list()))
    return board.list()


def build_notification(game_state, messages, game_status, player):
    print(f"[build_notification] Building notification for player [{player}] with status [{game_status}]")
    notification = Notification()
    notification.active = True
    random_message = str(random.randrange(3))

    if game_status == Status.DRAW:
        notification.title = messages.load("game.end.draw.header")
        notification.content = messages.load("game.end.draw." + random_message + ".message")
        notification.icon = messages.load("game.end.draw.icon")
        return notification

    player_won = (game_status == Status.PLAYER_ONE_WINS and player == 1) or \
                 (game_status == Status.PLAYER_TWO_WINS and player == 2)

    player_name = game_state["player_" + ("one" if player == 1 else "two")]["name"]

    if player_won:
        notification.title = messages.load_with_params("game.end.win.header", [player_name])
        notification.content = messages.load("game.end.win." + random_message + ".message")
        notification.icon = messages.load("game.end.win.icon")
        notification.mood = Mood.HAPPY.value
    else:
        notification.title = messages.load_with_params("game.end.lose.header", [player_name])
        notification.content = messages.load("game.end.lose." + random_message + ".message")
        notification.icon = messages.load("game.end.lose.icon")
        notification.mood = Mood.SAD.value

    return notification


def simulate_computer_think_time():
    thinking_time = random.randrange(4)
    print(f"[simulate_computer_think_time] Computer will think for [{thinking_time}] before placing move")
    time.sleep(thinking_time)
