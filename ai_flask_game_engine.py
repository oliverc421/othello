"""
Othello/Reversi

This is a python module which uses flask to provide a backend for a web-based 
Othello/Reversi game. It implements an AI opponent for the light player.

Global State:
- board: 2D list representing the current game state
- counter: Integer tracking remaining moves (starts at 60 for 64 squares minus 4 starting pieces)

Dependencies:
- Flask: Web framework for API endpoints
- components: Custom module with core Othello game logic

"""

from copy import deepcopy
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
    This function is called at the beginning of each turn to determine
    if the current player must pass or if the game should end.

    Args:
        colour: The player's colour as a string ('Light' or 'Dark ').
        board: The current game board as a 2D list of strings.
    
    Returns:
        True if at least one legal move exists for the given colour,
        False if no legal moves are available.
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
    and for deciding which move the AI should make.

    Args:
        board: The game board as a 2D list of strings ('Light', 'Dark ', or 'None ').

    Returns:
        A tuple (light_counters, dark_counters) where each is an integer
        representing the number of pieces of that colour on the board.
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

    Args:
        board: The final game board state as a 2D list.

    Returns:
        A formatted string announcing the game result, including:
        - "Game Over: Draw" if both players have equal pieces
        - "Game Over: Light wins" if Light has more pieces
        - "Game Over: Dark wins" if Dark has more pieces

    Note:
        This function only determines the winner based on piece count.
        The actual game over condition checking happens elsewhere.
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

    Args:
        colour: The colour of the player making the move ('Light' or 'Dark ').
        coordinate: A tuple (x, y) representing the coordinates to place the piece.
        board: The current game board to modify.

    Returns:
        The updated game board with the move applied and pieces flipped.

    Raises:
        No explicit exceptions, but assumes valid input coordinates.

    Process:
        1. Check all 8 directions around the placed piece
        2. For each direction, store the capture lines
        3. Flip all opponent pieces in the capture lines
        4. Update the board in place

    Note:
        This function modifies the board in place. For AI simulations,
        pass a deep copy of the board to avoid altering the game state. 
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
                            # times k by i and j to go in the direction of the opponent counters
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

def ai(board: list) -> tuple:

    """
    Determine the best move for the AI player (Light) using a greedy algorithm.
    
    The AI evaluates all legal moves available to Light and chooses the one that
    results in the maximum number of Light pieces on the board after the move.
    This is a simple greedy strategy that doesn't look ahead multiple moves.
    Args:

        board: The current game board as a 2D list.

    Returns:
        A tuple (x, y) representing the coordinates of the best move found,
        or (-1, -1) if no legal moves are available.
    """

    best_move = (-1, -1)
    best_score = -1
    for i in range(8):
        for j in range(8):
            if components.legal_move('Light', (i, j), board) is True:
                # copy otherwise possible_board would just be a reference to board
                possible_board = deepcopy(board)
                possible_board = swap_colours('Light', (i, j), possible_board)
                light_counters = (count_counters(possible_board))[0]
                # see how many counters light would have if it made this move
                if light_counters > best_score:
                    best_score = light_counters
                    best_move = (i, j)
    return best_move

@app.route('/')
def initialise_flask():

    """
    Initialize or reset the Flask application and game state.
    
    This route handler serves the main game interface and resets the game
    to its initial state. It's called when the user first visits the site
    or refreshes the page.

    Route:
    GET /

    Returns:
        A rendered HTML template with the initial game board.
    Side Effects:

        - Resets the global 'board' to the initial Othello setup
        - Resets the global 'counter' to 60 (remaining moves)
        - Serves the main game interface to the client
    Note:

        This function handles both initial game setup and game restart.
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

    Route:
        GET /move
    
    Query Parameters:
        x: Integer x-coordinate (0-7) of the player's move
        y: Integer y-coordinate (0-7) of the player's move

    Returns:
        JSON response with one of:
        - success: Move processed successfully with updated board
        - fail: Invalid move with error message
        - game_over: Game has ended with final result

    Process Flow:
        1. Validate player's move coordinates
        2. Check if move is legal for human player
        3. Apply move and flip pieces
        4. Check game over conditions
        5. Trigger AI move
        6. Update move counter
        7. Return updated game state
    """

    global board, counter
    print(counter)
    colour = 'Dark '    # dark goes first

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
    counter -= 1
    if move_is_available('Light', board) is False:
        if move_is_available('Dark ', board) is False:
            result = game_over(board)
            print(result)
        else:
            return jsonify({
            'status': 'success',
            'board': board,
            'player': 'Dark '
            })
    # call the ai function to get the coords for the ai move
    # then update the board
    board = swap_colours('Light', ai(board), board)
    counter -= 1

    if move_is_available('Light', board) is False:
        # if human can't move, prompt ai to move again
        # if ai also can't move, game over
        flag = False
        while flag is False:
            if move_is_available('Dark ', board) is False:
                if move_is_available('Light', board) is False:
                    result = game_over(board)
                    print(result)
                    return jsonify({
                    'status': 'success',
                    'board': board,
                    'player': 'None '
                    })
                else:
                    board = swap_colours('Light', ai(board), board)
                    counter -= 1
            else:
                flag = True

    # if succesful
    return jsonify({
    'status': 'success',
    'board': board,
    'player': 'Dark '
    })

if __name__ == '__main__':
    # Flask will start listening for HTTP requests on port 5000 (default)
    # debug=True allows the server to reload automatically on code changes
    app.run(debug=True)
