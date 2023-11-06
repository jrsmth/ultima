from src.app.model.board.board import Board
from src.app.model.square import Square


class ThreeBoard(Board):
    top_lhs = Square.NEUTRAL.value
    top_mid = Square.NEUTRAL.value
    top_rhs = Square.NEUTRAL.value
    mid_lhs = Square.NEUTRAL.value
    mid_mid = Square.NEUTRAL.value
    mid_rhs = Square.NEUTRAL.value
    bot_lhs = Square.NEUTRAL.value
    bot_mid = Square.NEUTRAL.value
    bot_rhs = Square.NEUTRAL.value

    def list(self):
        return [self.top_lhs, self.top_mid, self.top_rhs,
                self.mid_lhs, self.mid_mid, self.mid_rhs,
                self.bot_lhs, self.bot_mid, self.bot_rhs]
