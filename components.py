def initialise_board(size=8):
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
    for i in board:
        print(i)

def legal_move(colour: str, coordinate: tuple, board: list) -> bool:
    x, y = coordinate
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
                                else:
                                    return True
                        except IndexError:
                            break
            except IndexError:
                continue
    return False
