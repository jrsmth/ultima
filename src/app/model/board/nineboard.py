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
        return