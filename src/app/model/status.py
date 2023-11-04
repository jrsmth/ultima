from enum import Enum


class Status(Enum):
    IN_PROGRESS = 1
    DRAW = 2
    PLAYER_ONE_WINS = 3
    PLAYER_TWO_WINS = 4
