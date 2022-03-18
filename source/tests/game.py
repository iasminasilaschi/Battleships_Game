import unittest

from source.game.game import Game
from source.strategy.better_strategy import BetterStrategy


class TestGame(unittest.TestCase):
    """
    Test case class for domain
    """

    def setUp(self):
        """
        Prepare tests
        """
        self.strategy = BetterStrategy()
        self.game = Game(self.strategy)
        self.game.board.computer_board[1][2] = 'X'

    def test_human_move(self):
        self.assertRaises(Exception, self.game.human_move)
        self.assertIsNotNone(self.game.human_move(1, 4))
        self.assertEqual(str(self.game.human_move(1, 1)), "Move: (1, 1)")

    def test_computer_move(self):
        self.assertIsNotNone(self.game.computer_move())
