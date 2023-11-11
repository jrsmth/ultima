from src.app.model.board.board import Board
from src.app.model.board.threeboard import ThreeBoard


class NineBoard(Board):
    top_lhs = ThreeBoard()
    top_mid = ThreeBoard()
    top_rhs = ThreeBoard()
    mid_lhs = ThreeBoard()
    mid_mid = ThreeBoard()
    mid_rhs = ThreeBoard()
    bot_lhs = ThreeBoard()
    bot_mid = ThreeBoard()
    bot_rhs = ThreeBoard()

    def list(self):
        return [self.top_lhs.list(), self.top_mid.list(), self.top_rhs.list(),
                self.mid_lhs.list(), self.mid_mid.list(), self.mid_rhs.list(),
                self.bot_lhs.list(), self.bot_mid.list(), self.bot_rhs.list()]
