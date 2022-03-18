import unittest

from source.Board.board import Board
from source.domain.entities import Ship
from source.domain.validators import Validator


class TestBoard(unittest.TestCase):
    """
    Test case class for board
    """

    def setUp(self):
        """
        Prepare tests
        """
        self.validator = Validator()
        self.board = Board()
        self.board._computer_board[1][2] = 'X'
        self.board._player_board[3][4] = 'O'
        self.board._computer_board[5][6] = 'c'
        self.board._player_board[7][8] = 's'
        self.ship = Ship('c', 5, 1, 1, 'v')
        self.board.place_ship(self.ship, self.board.computer_board)

    def test_init(self):

        self.assertTrue(self.board.rows_count == self.board._rows == 10)
        self.assertTrue(self.board.columns_count == self.board._columns == 10)
        self.assertTrue(self.board._computer_length_carrier == self.board._player_length_carrier == 5)
        self.assertTrue(self.board._computer_length_battleship == self.board._player_length_battleship == 4)
        self.assertTrue(self.board._computer_length_destroyer == self.board._player_length_destroyer == 3)
        self.assertTrue(self.board._computer_length_submarine == self.board._player_length_submarine == 3)
        self.assertTrue(self.board._computer_length_patrol_boat == self.board._player_length_patrol_boat == 2)

    def test_get(self):
        self.assertEqual(self.board.get(1, 2, self.board.computer_board), 'X')
        self.assertEqual(self.board.get(3, 4, self.board.player_board), 'O')
        self.assertEqual(self.board.get(5, 6, self.board.computer_board), 'c')
        self.assertEqual(self.board.get(7, 8, self.board.player_board), 's')

    def test_is_free(self):
        self.assertTrue(self.board.is_free(2, 2, self.board.computer_board))
        self.assertFalse(self.board.is_free(7, 8, self.board.player_board))

    def test_is_valid(self):
        self.assertFalse(self.board.is_valid(1, 2, self.board.computer_board))
        self.assertTrue(self.board.is_valid(7, 8, self.board.player_board))

    def test_randomize_ship(self):
        self.assertIsNotNone(self.board.randomize_ship('c'))
        self.assertIsNotNone(self.board.randomize_ship('b'))
        self.assertIsNotNone(self.board.randomize_ship('d'))
        self.assertIsNotNone(self.board.randomize_ship('s'))
        self.assertIsNotNone(self.board.randomize_ship('p'))

    def test_find_ship_length(self):
        self.assertEqual(self.board.find_ship_length('c'), 5)
        self.assertEqual(self.board.find_ship_length('b'), 4)
        self.assertEqual(self.board.find_ship_length('d'), 3)
        self.assertEqual(self.board.find_ship_length('s'), 3)
        self.assertEqual(self.board.find_ship_length('p'), 2)

    def test_overlapping_ships(self):
        ship1 = Ship('p', 2, 1, 1, 'h')
        self.assertTrue(self.board.overlapping_ships(ship1, self.board.computer_board))
        ship2 = Ship('d', 3, 7, 7, 'h')
        self.assertFalse(self.board.overlapping_ships(ship2, self.board.computer_board))

    def test_computer_place_ships(self):
        self.assertEqual(self.board._ships, [])
        self.board.computer_place_ships()
        self.assertEqual(len(self.board._ships), 5)

    def test_move(self):
        self.assertEqual(str(self.board.move(1, 1, self.board.computer_board)), "Move: (1, 1)")

    def test_check_if_player_won(self):
        self.board._computer_length_carrier = 0
        self.board._computer_length_battleship = 0
        self.board._computer_length_destroyer = 0
        self.board._computer_length_submarine = 0
        self.board._computer_length_patrol_boat = 0
        self.assertTrue(self.board.check_if_player_won())
        self.board._computer_length_patrol_boat = 1
        self.assertFalse(self.board.check_if_player_won())

    def test_check_if_computer_won(self):
        self.board._player_length_carrier = 0
        self.board._player_length_battleship = 0
        self.board._player_length_destroyer = 0
        self.board._player_length_submarine = 0
        self.board._player_length_patrol_boat = 0
        self.assertTrue(self.board.check_if_computer_won())
        self.board._player_length_patrol_boat = 1
        self.assertFalse(self.board.check_if_computer_won())
