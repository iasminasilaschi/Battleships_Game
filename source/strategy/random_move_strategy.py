import random

from source.domain.entities import Move


class RandomMoveStrategy:
    def next_move(self, board):
        """
        Make a main, but valid move
        Randomly chooses a move from a set of valid moves
        :param board: the board class
        """
        # Store possible moves here
        available_moves = []

        for col in range(1, board.columns_count + 1):  # 1 - 10
            for row in range(1, board.rows_count + 1):  # 1 - 10
                if board.is_valid(row, col, board.player_board):
                    available_moves.append(Move(row, col, '0'))
        # Pick one of the available moves
        move = random.choice(available_moves)
        # print(move)
        return board.move(move.coordinate_x, move.coordinate_y, board.player_board)
