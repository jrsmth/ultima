from src.app.model.board.board import Board
from src.app.model.symbol import Symbol


class ThreeBoard(Board):
    top_lhs = Symbol.NEUTRAL.value
    top_mid = Symbol.NEUTRAL.value
    top_rhs = Symbol.NEUTRAL.value
    mid_lhs = Symbol.NEUTRAL.value
    mid_mid = Symbol.NEUTRAL.value
    mid_rhs = Symbol.NEUTRAL.value
    bot_lhs = Symbol.NEUTRAL.value
    bot_mid = Symbol.NEUTRAL.value
    bot_rhs = Symbol.NEUTRAL.value

    def list(self):
        return [self.top_lhs, self.top_mid, self.top_rhs,
                self.mid_lhs, self.mid_mid, self.mid_rhs,
                self.bot_lhs, self.bot_mid, self.bot_rhs]
