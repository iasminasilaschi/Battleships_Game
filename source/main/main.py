"""
BATTLESHIPS

Plan:
    1. Draw an empty board
    2. Let the user place its ships + randomly choose ship positions for the computer
    3. Alternate moves (computer moves)
    4. UI, win/lose condition

Classes:
    board
        - internal state of the board
        - move
            -> make a move on the board with X or O
            -> moves at A1 are forbidden
            -> return True iif at least 1 valid move remaining

    Strategy
        - computer "AI"
        - next_move(board) => return computer's next move

    game
        - has a board instance
        - human player move
        - computer move
            -> call a strategy for the computer player

    UI
        - has a game instance
        - has a Strategy instance
        - alternate play between human and computer
"""
from source.ui.console import UI

ui = UI()
ui.start()
