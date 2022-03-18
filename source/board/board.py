"""

No. 	Class of ship	   Size      Symbol
---------------------------------------------
1	    Carrier	            5           c
2	    Battleship	        4           b
3	    Destroyer	        3           d
4	    Submarine	        3           s
5	    Patrol Boat	        2           p

"""
import random

from texttable import Texttable

from source.domain.entities import Ship, Move
from source.domain.validators import Validator


class Board:
    def __init__(self):
        # the classical game of ships has a 10x10 board, so I'll set both the number of rows and columns to 10
        self.validator = Validator()
        self._rows = 10
        self._columns = 10
        self._computer_board = [[0 for col in range(self._columns + 2)] for row in range(self._rows + 2)]
        self._player_board = [[0 for col in range(self._columns + 2)] for row in range(self._rows + 2)]
        self._ships = []
        self._computer_length_carrier = 5
        self._computer_length_battleship = 4
        self._computer_length_destroyer = 3
        self._computer_length_submarine = 3
        self._computer_length_patrol_boat = 2
        self._player_length_carrier = 5
        self._player_length_battleship = 4
        self._player_length_destroyer = 3
        self._player_length_submarine = 3
        self._player_length_patrol_boat = 2

    @property
    def rows_count(self):
        return self._rows

    @property
    def columns_count(self):
        return self._columns

    @property
    def player_board(self):
        return self._player_board

    @property
    def computer_board(self):
        return self._computer_board

    def get(self, x, y, board):
        """
        Return symbol at position [x,y] on board
            'X'        -> found part of ship
            'O'        -> found nothing
            'c'        -> Carrier
            'b'        -> Battleship
            'd'        -> Destroyer
            's'        -> Submarine
            'p'        -> Patrol Boat
             0         -> empty square
        """
        return board[x][y]

    def is_free(self, x, y, board):
        """
        A cell is free if its value is 0
        :param x: coordinate x
        :param y: coordinate y
        :param board: computer board / player board
        :return: True if the cell is free, False otherwise
        """
        if self.get(x, y, board) == 0:
            return True
        return False

    def is_valid(self, x, y, board):
        """
        A cell is valid for making a move if it is either free (0) or contains part of a boat (c, b, d, s, p)
        If it contains O or X it means it was already hit, and if it contains a capital letter that is part of a boat
        (C, B, D, S, P) it means that that ship was already found and sunk, and the cell is therefore unavailable to be
        hit again
        :param x: coordinate x
        :param y: coordinate y
        :param board: computer / player board
        :return: True if it is valid, False otherwise
        """
        cell = self.get(x, y, board)
        if cell != 'O' and cell != 'X' and cell != 'C' and cell != 'B' and cell != 'D' and cell != 'S' and cell != 'P':
            return True
        return False

    def randomize_ship(self, symbol):
        """
        According to the type of ship it is, given by its unique symbol, its specific length is found out and
        the ship instance is created and will be placed on the computer board
        It is given a randomized starting cell denoted by a x and a y coordinate and an orientation, either
        h -> horizontal, v -> vertical
        :param symbol: a characterizing symbol for the type of ship, its first letter (see lines 1-10)
        :return: the ship instance
        """
        length = self.find_ship_length(symbol)
        coordinate_x = random.randint(1, 10)
        coordinate_y = random.randint(1, 10)
        possible_orientations = ['h', 'v']  # h -> horizontal, v -> vertical
        orientation = random.choice(possible_orientations)
        ship = Ship(symbol, length, coordinate_x, coordinate_y, orientation)
        return ship

    def find_ship_length(self, symbol):
        """
        According to its unique symbol, the ship length is found out (see lines 1-10)
        :param symbol: a characterizing symbol for the type of ship, its first letter (see lines 1-10)
        :return: the length for the ship that was searched for
        """
        length = 0
        if symbol == 'c':
            length = self._computer_length_carrier
        elif symbol == 'b':
            length = self._computer_length_battleship
        elif symbol == 'd':
            length = self._computer_length_destroyer
        elif symbol == 's':
            length = self._computer_length_submarine
        elif symbol == 'p':
            length = self._computer_length_patrol_boat
        return length

    def overlapping_ships(self, ship, board):
        """
        Checks if the ship we wish to place would overlap on an already existent ship
        :param ship: a ship instance composed of symbol, length, x coordinate, y coordinate, orientation
        :param board: computer / player board
        :return: True if they overlap, False otherwise
        """
        x = ship.coordinate_x
        y = ship.coordinate_y
        if ship.orientation == 'h':
            for each_cell in range(ship.length):
                if not self.is_free(ship.coordinate_x, y, board):
                    return True
                y += 1
        elif ship.orientation == 'v':
            for each_cell in range(ship.length):
                if not self.is_free(x, ship.coordinate_y, board):
                    return True
                x += 1
        return False

    def computer_place_ships(self):
        """
        The computer randomly tries to place the 5 ships until each of their positions are valid
        :return: the computer board is updated with the corresponding symbols in the randomly chose cells
        """
        symbols = ['c', 'b', 'd', 's', 'p']
        for symbol in symbols:
            ship = self.randomize_ship(symbol)
            valid = False
            while not valid:
                if self.validator.validate(ship):
                    if not self.overlapping_ships(ship, self._computer_board):
                        valid = True
                if valid is False:
                    ship = self.randomize_ship(symbol)
            self._ships.append(ship)
            self.place_ship(ship, self._computer_board)

    def player_place_ships(self, symbol, coordinate_x, coordinate_y, orientation):
        """
        Tries to place the ships wanted by the player in the cells wnated by the player until the position is valid
        :param symbol: provided by the player, a characterizing symbol for the type of ship, its first letter
                       (see lines 1-10)
        :param coordinate_x: provided by the player, the x coordinate = row
        :param coordinate_y: provided by the player, the y coordinate = column
        :param orientation: provided by the player, h -> horizontal, v -> vertical
        :return: the player board is updated with the symbols in the corresponding cells
        """
        length = self.find_ship_length(symbol)
        ship = Ship(symbol, length, coordinate_x, coordinate_y, orientation)
        valid = False
        while not valid:
            if self.validator.validate(ship):
                if not self.overlapping_ships(ship, self._player_board):
                    valid = True
            if valid is False:
                return False
        self.place_ship(ship, self._player_board)
        return True

    def place_ship(self, ship, board):
        """
        Places the ships on both boards by putting the corresponding ship symbol in each cell
        :param ship: a ship instance composed of symbol, length, x coordinate, y coordinate, orientation
        :param board: computer / player board
        :return: the board is updated with the symbols in the corresponding cells
        """
        row = ship.coordinate_x
        column = ship.coordinate_y
        if ship.orientation == 'h':
            for each_cell in range(ship.length):
                board[row][column] = ship.symbol
                column += 1
        elif ship.orientation == 'v':
            for each_cell in range(ship.length):
                board[row][column] = ship.symbol
                row += 1

    def move(self, x, y, board):
        """
        Making a move - both for player and computer
        :param x: x coordinate
        :param y: y coordinate
        :param board: computer / player board
        :return: the move that was made in a nice format: (x, y)
        """
        if self.is_free(x, y, board):
            board[x][y] = 'O'
            symbol = '0'
        else:
            symbol = board[x][y]
            board[x][y] = 'X'
        move = Move(x, y, symbol)
        return move

    def analyse_move(self, move, board):
        """
        Analyses weather something has been hit or not, and if it has been, it also checks it that ship was sunk
        :param move: the move to be analysed
        :param board: computer / player board
        :return: the move analysis - a message for the user that will be printed in the ui layer
        """
        if move.symbol != '0':
            move_analysis = self.check_if_boat_has_sunk(move.symbol, board)
        else:
            move_analysis = "Nothing there!"
        return move_analysis

    def check_if_boat_has_sunk(self, symbol, board):
        """
        Checks both for the computer board and for the player board is the length of the corresponding ship is 0
        If it is, it means that the respective ship has sunk and the move analysis updates itself by adding a
        corresponding message that will eventually be printed in the ui layer on the console
        :param symbol: a characterizing symbol for the type of ship, its first letter (see lines 1-10)
        :param board: player / computer board
        :return: an updated message in case one of the lengths is 0, or just the initial message otherwise
        """
        move_analysis = "Something was hit!"
        if symbol == 'c':
            if board == self._computer_board:
                self._computer_length_carrier -= 1
                if self._computer_length_carrier == 0:
                    move_analysis = move_analysis + "\nCarrier sunk!"
                    for ship in self._ships:
                        if ship.symbol == 'c':
                            ship.symbol = 'C'
                            self.place_ship(ship, self._computer_board)
            else:
                self._player_length_carrier -= 1
                if self._player_length_carrier == 0:
                    move_analysis = move_analysis + "\nCarrier sunk!"
        elif symbol == 'b':
            if board == self._computer_board:
                self._computer_length_battleship -= 1
                if self._computer_length_battleship == 0:
                    move_analysis = move_analysis + "\nBattleship sunk!"
                    for ship in self._ships:
                        if ship.symbol == 'b':
                            ship.symbol = 'B'
                            self.place_ship(ship, self._computer_board)
            else:
                self._player_length_battleship -= 1
                if self._player_length_battleship == 0:
                    move_analysis = move_analysis + "\nBattleship sunk!"
        elif symbol == 'd':
            if board == self._computer_board:
                self._computer_length_destroyer -= 1
                if self._computer_length_destroyer == 0:
                    move_analysis = move_analysis + "\nDestroyer sunk!"
                    for ship in self._ships:
                        if ship.symbol == 'd':
                            ship.symbol = 'D'
                            self.place_ship(ship, self._computer_board)
            else:
                self._player_length_destroyer -= 1
                if self._player_length_destroyer == 0:
                    move_analysis = move_analysis + "\nDestroyer sunk!"
        elif symbol == 's':
            if board == self._computer_board:
                self._computer_length_submarine -= 1
                if self._computer_length_submarine == 0:
                    move_analysis = move_analysis + "\nSubmarine sunk!"
                    for ship in self._ships:
                        if ship.symbol == 's':
                            ship.symbol = 'S'
                            self.place_ship(ship, self._computer_board)
            else:
                self._player_length_submarine -= 1
                if self._player_length_submarine == 0:
                    move_analysis = move_analysis + "\nSubmarine sunk!"
        elif symbol == 'p':
            if board == self._computer_board:
                self._computer_length_patrol_boat -= 1
                if self._computer_length_patrol_boat == 0:
                    move_analysis = move_analysis + "\nPatrol boat sunk!"
                    for ship in self._ships:
                        if ship.symbol == 'p':
                            ship.symbol = 'P'
                            self.place_ship(ship, self._computer_board)
            else:
                self._player_length_patrol_boat -= 1
                if self._player_length_patrol_boat == 0:
                    move_analysis = move_analysis + "\nPatrol boat sunk!"
        return move_analysis

    def check_if_computer_won(self):
        """
        Checks if the game ended and the computer won by comparing each of the player's ship length with 0
        If they are all 0, that means there are no more ships to be sunk, and therefore the computer won
        :return: True if all of the lengths of the ships are 0, False otherwise
        """
        if self._player_length_carrier == 0 and self._player_length_battleship == 0 and \
                self._player_length_destroyer == 0 and self._player_length_submarine == 0 and \
                self._player_length_patrol_boat == 0:
            return True
        return False

    def check_if_player_won(self):
        """
        Checks if the game ended and the player won by comparing each of the computer's ship length with 0
        If they are all 0, that means there are no more ships to be sunk, and therefore the player won
        :return: True if all of the lengths of the ships are 0, False otherwise
        """
        if self._computer_length_carrier == 0 and self._computer_length_battleship == 0 and \
                self._computer_length_destroyer == 0 and self._computer_length_submarine == 0 and \
                self._computer_length_patrol_boat == 0:
            return True
        return False

    def str_computer_board(self):
        """
        For printing the computer board nicely
        :return: the str() version of the computer board
        """
        computer_table = Texttable()
        header = [' ']
        for coordinate_letter in range(self._columns):
            header.append(chr(65 + coordinate_letter))
        computer_table.header(header)
        for row in range(1, self._rows + 1):
            visible_computer_board = []

            for val in self._computer_board[row][1:-1]:
                if val == 'X':
                    visible_computer_board.append('X')
                elif val == 'C':
                    visible_computer_board.append('C')
                elif val == 'B':
                    visible_computer_board.append('B')
                elif val == 'D':
                    visible_computer_board.append('D')
                elif val == 'S':
                    visible_computer_board.append('S')
                elif val == 'P':
                    visible_computer_board.append('P')
                elif val == 'O':
                    visible_computer_board.append('O')
                else:
                    visible_computer_board.append(' ')

                # if val == 0:
                #     visible_computer_board.append(' ')
                # else:
                #     visible_computer_board.append(val)

            computer_table.add_row([row] + visible_computer_board)
        return "\nComputer board:\n" + computer_table.draw()

    def str_player_board(self):
        """
        For printing the player board nicely
        :return: the str() version of the player board
        """
        player_table = Texttable()
        header = [' ']
        for coordinate_letter in range(self._columns):
            header.append(chr(65 + coordinate_letter))
        player_table.header(header)
        for row in range(1, self._rows + 1):
            visible_player_board = []

            for val in self._player_board[row][1:-1]:

                #     if val == 'X':
                #         visible_player_board.append('X')
                #     elif val == 'C':
                #         visible_player_board.append('C')
                #     elif val == 'B':
                #         visible_player_board.append('B')
                #     elif val == 'D':
                #         visible_player_board.append('D')
                #     elif val == 'S':
                #         visible_player_board.append('S')
                #     elif val == 'P':
                #         visible_player_board.append('P')
                #     elif val == 'O':
                #         visible_player_board.append('O')
                #     else:
                #         visible_player_board.append(' ')

                if val == 0:
                    visible_player_board.append(' ')
                else:
                    visible_player_board.append(val)
            player_table.add_row([row] + visible_player_board)
        return "\nPlayer board:\n" + player_table.draw()
