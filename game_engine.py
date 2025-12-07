import components

def cli_coords_input() -> tuple:
    x, y = 8, 8
    while not (0<=x<=7 and 0<=y<=7):
        try:
            x = int(input("Input your x coordinate: "))
            assert 0<=x<=7
            y = int(input("Input your y coordinate: "))
            assert 0<=y<=7
        except (ValueError, AssertionError):
            print("You must enter a number between 0 and 7")
    coords = (x, y)
    return coords

def move_is_available(colour: str, board: list) -> bool:
    for i in range(8):
        for j in range(8):
            move_available = components.legal_move(colour, (i, j), board)
            if move_available == True:
                return True
    return False    # if we complete the full loop and have not returned true,                  then we have checked every square and not found a legal move

def count_counters(board: list) -> tuple:
    light_counters = 2
    dark_counters = 2
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'Light':
                light_counters += 1
            elif board[i][j] == 'Dark ':
                dark_counters += 1
            else:
                pass
    return (light_counters, dark_counters)

def game_over(board: list):
    print("Game over")
    light_counters, dark_counters = count_counters(board)
    if light_counters == dark_counters:
        print('Draw')
    elif light_counters > dark_counters:
        print('Light wins')
    else:
        print('Dark wins')
    quit()

def swap_colours(colour: str, coordinate: tuple, board: list) -> list:
    directions_to_go_in = []
    squares_to_change = [coordinate]
    x, y = coordinate
    if colour == 'Light':
        opponent = 'Dark '
    else:
        opponent = 'Light'
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            try:
                # check for negative indices
                if (y + i) < 0 or (x + j) < 0:
                    raise IndexError("Negative index")
                if board[y + i][x + j] == opponent:
                    for k in range(1, 8):
                        try:
                            # check for negative indices
                            if (y + k * i) < 0 or (x + k * j) < 0:
                                raise IndexError("Negative index")
                            if board[y + k * i][x + k * j] != opponent:
                                if board[y + k * i][x + k * j] == 'None ':
                                    break
                                directions_to_go_in.append((i, j))
                                break
                        except IndexError:
                            break
            except IndexError:
                continue

    for direction in directions_to_go_in:
        i, j = direction
        for squares in range(1, 8):
            new_y = y + squares * i
            new_x = x + squares * j

            # check bounds for squares_to_change too
            if 0 <= new_y < len(board) and 0 <= new_x < len(board[0]):
                if board[new_y][new_x] == opponent:
                    squares_to_change.append((new_x, new_y))
                else:
                    break
            else:
                break

    for square in squares_to_change:
        board[square[1]][square[0]] = colour

    return board


def simple_game_loop():
    print("Welcome to Othello")
    board = components.initialise_board()
    counter = 60
    while True:
        components.print_board(board)
        if counter % 2 == 0:    # if counter is even
            colour, opponent = 'Dark ', 'Light'    # dark goes first
        else:
            colour, opponent = 'Light', 'Dark '
        if move_is_available(colour, board) == False:    # check that this colour can move
            colour, opponent = opponent, colour    # if no move available then swap colours
        if move_is_available(colour, board) == False:    # check the other colour can move
            game_over(board)            # if neither can move, game over
        flag = False
        while flag == False:
            coords = cli_coords_input()
            flag = components.legal_move(colour, coords, board)
            if flag == False:
                print("This is not a legal move. Select different coordinates.")
        board = swap_colours(colour, coords, board)
        counter -= 1
        if counter == 0:
            game_over(board)

if __name__ == '__main__':
    simple_game_loop()
