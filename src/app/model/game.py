import shortuuid

from src.app.model.base import Base
from src.app.model.board.nineboard import NineBoard
from src.app.model.board.threeboard import ThreeBoard
from src.app.model.mode.gamemode import GameMode
from src.app.model.mode.playermode import PlayerMode
from src.app.model.notification import Notification
from src.app.model.player import Player
from src.app.model.status import Status
from src.app.model.symbol import Symbol


# Model object that holds the state of a game
class Game(Base):  # Question :: Rename? -> State?
    complete = False
    game_id = ''
    game_mode = GameMode.STANDARD.value
    player_one = Player('', Symbol.CROSS.value, Notification())
    player_two = Player('', Symbol.CIRCLE.value, Notification())
    player_turn = 1  # Tracks whose turn it is: player '1' or '2' -> # Question :: better way?
    player_mode = PlayerMode.DOUBLE
    playable_square = -1  # Tracks the next outer square that can be played (ultimate-mode); -1 represents any square
    outer_states = [  # List of states for each outer square -> # Question :: better way?
        Status.IN_PROGRESS.value, Status.IN_PROGRESS.value, Status.IN_PROGRESS.value,
        Status.IN_PROGRESS.value, Status.IN_PROGRESS.value, Status.IN_PROGRESS.value,
        Status.IN_PROGRESS.value, Status.IN_PROGRESS.value, Status.IN_PROGRESS.value
    ]


def has_valid_game_id(game_id):
    if game_id != "-1":  # Does game id already exist?
        return True
    else:
        return False


def generate_game_id():
    return shortuuid.uuid()[:12]


def generate_board(game_mode):
    if game_mode == GameMode.STANDARD.value:
        return ThreeBoard().list()
    elif game_mode == GameMode.ULTIMATE.value:
        return NineBoard().list()
    else:
        print("Game Mode already set [" + game_mode + "]")  # TODO :: err handle
