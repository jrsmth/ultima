from src.app.model.base import Base
from src.app.model.mode.gamemode import GameMode
from src.app.model.mode.playermode import PlayerMode
from src.app.model.player import Player
from src.app.model.status import Status
from src.app.model.symbol import Symbol


# Model object that holds the state of a game
class Game(Base):  # Question :: Rename? -> State?
    complete = False
    game_id = ''
    game_mode = GameMode.STANDARD
    player_one = Player('', Symbol.CROSS.value)
    player_two = Player('', Symbol.CIRCLE.value)
    player_turn = 1  # Tracks whose turn it is: player '1' or '2' -> # Question :: better way?
    player_mode = PlayerMode.DOUBLE
    playable_square = -1  # Tracks the next outer square that can be played (ultimate-mode); -1 represents any square
    outer_states = [  # List of states for each outer square -> # Question :: better way?
        Status.IN_PROGRESS.value, Status.IN_PROGRESS.value, Status.IN_PROGRESS.value,
        Status.IN_PROGRESS.value, Status.IN_PROGRESS.value, Status.IN_PROGRESS.value,
        Status.IN_PROGRESS.value, Status.IN_PROGRESS.value, Status.IN_PROGRESS.value
    ]
