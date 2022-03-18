class InputException(Exception):
    pass


class Validator:
    @staticmethod
    def validate(ship):
        if ship.orientation == 'h':
            max_ship_coordinate_y = ship.coordinate_y + ship.length
            if max_ship_coordinate_y - 1 > 10:
                return False
        elif ship.orientation == 'v':
            max_ship_coordinate_x = ship.coordinate_x + ship.length
            if max_ship_coordinate_x - 1 > 10:
                return False
        return True

    @staticmethod
    def validate_cell(column, row):
        if column < 1 or column > 10:
            raise InputException("Column should be between A and J!")
        if row < 1 or row > 10:
            raise InputException("Row should be between 1 and 10!")

    @staticmethod
    def validate_symbol(symbol):
        if symbol != 'c' and symbol != 'b' and symbol != 'd' and symbol != 's' and symbol != 'p':
            raise InputException("The boat with this initial is not available!")

    @staticmethod
    def validate_orientation(orientation):
        if orientation != 'h' and orientation != 'v':
            raise InputException("This orientation doesn't exist... yet, at least!")