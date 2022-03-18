from source.domain.validators import Validator
from source.game.game import Game
from source.strategy.better_strategy import BetterStrategy


class UI:
    def __init__(self):
        self._strategy = BetterStrategy()
        self._game = Game(self._strategy)
        self._validator = Validator()

    def read_human_ship_information(self):
        symbol = input("\nType the symbol of the ship you wish to place: ").strip().lower()
        self._validator.validate_symbol(symbol)
        coordinates = self.read_human_move()
        coordinate_x = coordinates[1]
        coordinate_y = coordinates[0]
        orientation = input("h -> horizontal \nv -> vertical \nType the orientation: ").strip().lower()
        self._validator.validate_orientation(orientation)
        return symbol, coordinate_x, coordinate_y, orientation

    def print_available_ships(self, ships_available):
        print("\nSymbol 	Class of ship	   Size")
        print("---------------------------------")
        for symbol in ships_available:
            if symbol == 'c':
                print("c	    Carrier	            5")
            if symbol == 'b':
                print("b	    Battleship	        4")
            if symbol == 'd':
                print("d	    Destroyer	        3")
            if symbol == 's':
                print("s	    Submarine	        3")
            if symbol == 'p':
                print("p	    Patrol Boat	        2")

    def read_human_move(self):
        # TODO Add error handling
        coord = input("\nType the coordinates: ").strip()
        if '1' <= coord[0] <= '9' and coord[1] != '0':
            row = int(coord[0])
            column = ord(coord[1].lower()) - 96
        elif coord[0] == '1' and coord[1] == '0':
            row = int(coord[0] + coord[1])
            column = ord(coord[2].lower()) - 96
        else:
            row = int(coord[1:])
            # Calculate column index from character's ASCII code
            column = ord(coord[0].lower()) - 96
        self._validator.validate_cell(column, row)
        return column, row

    def ui_player_place_ships(self):
        ships_available = ['c', 'b', 'd', 's', 'p']
        print(self._game.board.str_player_board())
        player_ships_placed = False
        while not player_ships_placed:
            try:
                self.print_available_ships(ships_available)
                ship_information = self.read_human_ship_information()
                if self._game.board.player_place_ships(*ship_information):
                    symbol = ship_information[0]
                    index_to_be_removed = None
                    for index in range(len(ships_available)):
                        if ships_available[index] == symbol:
                            index_to_be_removed = index
                    del ships_available[index_to_be_removed]
                    if len(ships_available) == 0:
                        player_ships_placed = True
                else:
                    print("Invalid place!")
                print(self._game.board.str_player_board())
            except Exception as exception:
                print(exception)

    def start(self):
        finished = False
        human_turn = True
        # Human places boats
        self.ui_player_place_ships()
        # Calculator places boats randomly
        self._game.board.computer_place_ships()
        player_move = ""
        player_move_analysis = "game started! Make your first move!"

        while not finished:
            try:
                if human_turn:
                    print(self._game.board.str_computer_board())
                    print(player_move)
                    print(player_move_analysis)
                    coord = self.read_human_move()
                    player_move = self._game.human_move(coord[1], coord[0])
                    player_move_analysis = self._game.board.analyse_move(player_move, self._game.board.computer_board)
                    if self._game.board.check_if_player_won() is True:
                        print(self._game.board.str_computer_board())
                        print("Congrats, you won!")
                        finished = True
                else:
                    computer_move = self._game.computer_move()
                    print(self._game.board.str_player_board())
                    computer_move_analysis = self._game.board.analyse_move(computer_move, self._game.board.player_board)
                    print(computer_move)
                    print(computer_move_analysis)
                    if self._game.board.check_if_computer_won() is True:
                        print("Sorry, you lost!")
                        finished = True
                human_turn = not human_turn
            except Exception as exception:
                print(exception)
