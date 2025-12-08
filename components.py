"""
This is the module which stores the functions for 
initialising the board and checking for legal moves
"""

def initialise_board():
    """
    Initialises the board
    
    Returns:
        The board as a 2D array
    """

    board = [['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
         ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
         ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
         ['None ', 'None ', 'None ', 'Light', 'Dark ', 'None ', 'None ', 'None '],
         ['None ', 'None ', 'None ', 'Dark ', 'Light', 'None ', 'None ', 'None '],
         ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
         ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
         ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ']]
    return board

def print_board(board):
    """
    prints the board
    """
    for i in board:
        print(i)

def legal_move(colour: str, coordinate: tuple, board: list) -> bool:

    """ 
    Check if a certain move is legal according to Othello rules
    This function checks each adjacent square to coordinate and finds an opponent counter
    When opponent counter found, iterate in direction of opponent counter until ally counter found
    
    Args:
        colour: The player's colour as a string ('Light' or 'Dark ').
        coordinate: The square the player as clicked on, as a tuple
        board: The current game board as a 2D list of strings.

    Returns:
        True if move is legal
        False if not
    """

    x, y = coordinate
    # check for invalid coords
    if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board):
        return False

    if board[y][x] != 'None ':
        return False
    if colour == 'Light':
        opponent = 'Dark '
    else:
        opponent = 'Light'

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # skip checking the current square

            try:
                # check if indices would be negative (which Python allows but shouldn't)
                if (y + i) < 0 or (x + j) < 0:
                    raise IndexError("Negative index")

                if board[y + i][x + j] == opponent:
                    for k in range(1, 8):
                        try:
                            # check if indices would be negative again
                            if (y + k * i) < 0 or (x + k * j) < 0:
                                raise IndexError("Negative index")

                            if board[y + k * i][x + k * j] != opponent:
                                if board[y + k * i][x + k * j] == 'None ':
                                    break
                                return True
                        except IndexError:
                            break
            except IndexError:
                continue
    return False
