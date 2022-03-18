import random

from source.domain.entities import Move


class BetterStrategy:
    def __init__(self):
        self.last_move = None

    def next_good_move(self, board):
        """
        If something was hit, it should keep looking in the proximity of that square.
        Otherwise, just chooses a random move from a set of valid moves.
        :param board: the board class
        """
        # Store possible moves here
        available_moves = []

        for col in range(1, board.columns_count + 1):  # 1 - 10
            for row in range(1, board.rows_count + 1):  # 1 - 10
                if board.is_valid(row, col, board.player_board):
                    available_moves.append(Move(row, col, '0'))
        # Pick one of the available moves
        if self.last_move is None or self.last_move.symbol == '0':
            move = random.choice(available_moves)
        else:
            x = self.last_move.coordinate_x
            y = self.last_move.coordinate_y
            good_moves = self.find_good_moves(board, x, y)
            if good_moves:
                move = random.choice(good_moves)
            else:
                move = random.choice(available_moves)
        self.last_move = board.move(move.coordinate_x, move.coordinate_y, board.player_board)
        return self.last_move

    def find_good_moves(self, board, x, y):
        """
        Validates potential good moves (up, down, left or right of the hit cell) and appends them to a list
        :param board: the board class
        :param x: the x coordinate = row
        :param y: the y coordinate = column
        :return: a list of good moves
        """
        good_moves = []
        if x + 1 <= 10 and board.is_valid(x + 1, y, board.player_board):
            good_moves.append(Move(x + 1, y, '0'))
        if x - 1 >= 1 and board.is_valid(x - 1, y, board.player_board):
            good_moves.append(Move(x - 1, y, '0'))
        if y + 1 <= 10 and board.is_valid(x, y + 1, board.player_board):
            good_moves.append(Move(x, y + 1, '0'))
        if y - 1 >= 1 and board.is_valid(x, y - 1, board.player_board):
            good_moves.append(Move(x, y - 1, '0'))
        return good_moves
