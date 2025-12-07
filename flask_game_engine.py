"""
Othello/Reversi

This is a python module which uses flask to provide a backend for a web-based
Othello/Reversi game.
"""

from flask import Flask, render_template, request, jsonify
import components

app = Flask(__name__)

counter = 60
board = components.initialise_board()

def move_is_available(colour: str, board: list) -> bool:

    """
    Check if a player has at least one legal move available on the current board.
    This function iterates through all 64 squares on the board, using the legal_move
    function to test each position. It returns as soon as any legal move is found,
    """

    for i in range(8):
        for j in range(8):
            move_available = components.legal_move(colour, (i, j), board)
            if move_available is True:
                return True
    return False

def count_counters(board: list) -> tuple:

    """
    Count the number of pieces each player has on the board.
    This function is used for determining the winner when the game ends,
    """

    light_counters = 0
    dark_counters = 0
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

    """
    This function outputs the winner based on how many counters
    of each colour are on the board when there are no more moves available
    """

    light_counters, dark_counters = count_counters(board)
    if light_counters == dark_counters:
        result = 'Draw'
    elif light_counters > dark_counters:
        result = 'Light wins'
    else:
        result = 'Dark wins'
    return f"Game Over: {result}"

def swap_colours(colour: str, coordinate: tuple, board: list) -> list:

    """
    This function applies a move to the board and flip all captured opponent pieces.
    It places a piece of the given colour at the specified coordinate, then
    identifies and flips all opponent pieces that are captured in straight lines
    (horizontal, vertical, and diagonal).
    """

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

@app.route('/')
def initialise_flask():

    """
    Initialize or reset the Flask application and game state.

    This route handler serves the main game interface and resets the game
    to its initial state. It's called when the user first visits the site
    or refreshes the page.
    """

    global board, counter
    # we initialise counter again here in case the user restarts
    counter = 60
    board = components.initialise_board()
    return render_template('index.html', game_board=board)

@app.route('/move')
def get_move():

    """
    Process a player's move and the AI's response in a single HTTP request.

    This is the main game loop handler. It validates the player's move,
    applies it to the board, then triggers the AI to make its move.
    Handles game over conditions and turn management.
    """

    global board, counter
    print(counter)

    if counter % 2 == 0:    # if counter is even
        colour, opponent = 'Dark ', 'Light'    # dark goes first
    else:
        colour, opponent = 'Light', 'Dark '


    if move_is_available(colour, board) is False:    # check that this colour can move
        colour, opponent = opponent, colour    # if no move available then swap colours
    if move_is_available(colour, board) is False:    # check the other colour can move
        result = game_over(board)            # if neither can move, game over
        print(result)

    # get player input
    try:
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        coords = (x, y)
    except (TypeError, ValueError):
    # return an error if coordinates are missing or invalid
        return jsonify({'status': 'fail', 'message': 'Invalid coordinates received.'})

    if components.legal_move(colour, coords, board) is False:
        message = "This is not a legal move. Select different coordinates."
        return jsonify({'status': 'fail', 'message': message})
    # if move is legal, update the board
    board = swap_colours(colour, coords, board)

    # we check again that the move is available because if the board is full then the
    # /move route cannot be called again, so there is no way to check the board is full
    # after the final counter has been placed, unless we do it at the end of this function
    if move_is_available('Dark ', board) is False and move_is_available('Light', board) is False:
        result = game_over(board)
        print(result)


    counter -= 1

    # if succesful
    return jsonify({
    'status': 'success',
    'board': board,
    'player': opponent
    })

if __name__ == '__main__':
    # Flask will start listening for HTTP requests on port 5000 (default)
    # debug=True allows the server to reload automatically on code changes
    app.run(debug=True)
