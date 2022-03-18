import unittest

from source.Board.board import Board
from source.strategy.better_strategy import BetterStrategy


class TestStrategy(unittest.TestCase):
    """
    Test case class for domain
    """

    def setUp(self):
        """
        Prepare tests
        """
        self.strategy = BetterStrategy()
        self.board = Board()

    def test_next_good_move(self):
        move = self.strategy.next_good_move(self.board)
        self.assertIsNotNone(move)

    def test_find_good_moves(self):
        good_moves = self.strategy.find_good_moves(self.board, 1, 1)
        self.assertIsNotNone(good_moves)
