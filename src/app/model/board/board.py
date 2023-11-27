from abc import ABC, abstractmethod

from src.app.model.status import Status
from src.app.model.symbol import Symbol


class Board(ABC):

    @property
    @abstractmethod
    def top_lhs(self): pass
    # Top Left-Hand Side (0)

    @property
    @abstractmethod
    def top_mid(self): pass
    # Top Middle (1)

    @property
    @abstractmethod
    def top_rhs(self): pass
    # Top Right-Hand Side (2)

    @property
    @abstractmethod
    def mid_lhs(self): pass
    # Middle Left-Hand Side (3)

    @property
    @abstractmethod
    def mid_mid(self): pass
    # Middle Middle (4)

    @property
    @abstractmethod
    def mid_rhs(self): pass
    # Middle Right-Hand Side (5)

    @property
    @abstractmethod
    def bot_lhs(self): pass
    # Bottom Left-Hand Side (6)

    @property
    @abstractmethod
    def bot_mid(self): pass
    # Bottom Middle (7)

    @property
    @abstractmethod
    def bot_rhs(self): pass
    # Bottom Right-Hand Side (8)

    @abstractmethod
    def list(self): pass
    # Returns list in the form [top_lhs, top_mid, ...]


# Maps the status of an outer square to the corresponding player symbol
def map_to_symbol(state):
    if state == Status.IN_PROGRESS.value or state == Status.DRAW.value:
        return Symbol.NEUTRAL.value
    if state == Status.PLAYER_ONE_WINS.value:
        return Symbol.CROSS.value
    if state == Status.PLAYER_TWO_WINS.value:
        return Symbol.CIRCLE.value
