from source.board.board import Board


class Game:
    def __init__(self, strategy):
        self._board = Board()
        self._strategy = strategy

    @property
    def board(self):
        return self._board

    def human_move(self, x, y):
        """
        Checks if the move the player wants to make is valid, and if it is, performs it
        :param x: the x coordinate = row
        :param y: the y coordinate = column
        :return: the move made in the format (x, y)
        """
        if self._board.is_valid(x, y, self._board.computer_board):
            move = self._board.move(x, y, self._board.computer_board)
            return move
        raise Exception("You cannot hit here again!")

    def computer_move(self):
        """
        The strategy chosen for the computer is the better one
        Performs the move chose by the computer
        :return: the move made in the format (x, y)
        """
        move = self._strategy.next_good_move(self._board)
        return move
