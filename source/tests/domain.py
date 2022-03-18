import unittest

from source.domain.entities import Ship, Move


class TestDomain(unittest.TestCase):
    """
    Test case class for domain
    """

    def setUp(self):
        """
        Prepare tests
        """
        self.ship = Ship('c', 5, 1, 2, 'v')
        self.move = Move(3, 4, 'O')

    def test_ship(self):
        self.assertEqual(self.ship.symbol, 'c')
        self.assertEqual(self.ship.coordinate_x, 1)
        self.assertEqual(self.ship.coordinate_y, 2)
        self.assertEqual(self.ship.orientation, 'v')
        self.assertEqual(self.ship.length, 5)
        self.ship.coordinate_x = 3
        self.ship.coordinate_y = 4
        self.assertEqual(self.ship.coordinate_x, 3)
        self.assertEqual(self.ship.coordinate_y, 4)

    def test_move(self):
        self.assertEqual(self.move.symbol, 'O')
        self.assertEqual(self.move.coordinate_x, 3)
        self.assertEqual(self.move.coordinate_y, 4)
        self.move.coordinate_x = 5
        self.move.coordinate_y = 6
        self.assertEqual(self.move.coordinate_x, 5)
        self.assertEqual(self.move.coordinate_y, 6)
