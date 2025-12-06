import components
from copy import deepcopy
from time import sleep
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

counter = 60
board = components.initialise_board()

def move_is_available(colour: str, board: list) -> bool:
    for i in range(8):
        for j in range(8):
            move_available = components.legal_move(colour, (i, j), board)
            if move_available == True:
                return True
    return False    # if we complete the full loop and have not returned true, then we have checked every square and not found a legal move

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
    light_counters, dark_counters = count_counters(board)
    if light_counters == dark_counters:
        result = ('Draw')
    elif light_counters > dark_counters:
        result = ('Light wins')
    else:
        result = ('Dark wins')
    return f"Game Over: {result}"

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
                                else:
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
    best_move = (-1, -1) 
    best_score = -1
    for i in range(8):
        for j in range(8):
            if components.legal_move('Light', (i, j), board) is True:
                possible_board = deepcopy(board) # copy otherwise possible_board would just be a reference to the same list
                possible_board = swap_colours('Light', (i, j), possible_board)
                light_counters = (count_counters(possible_board))[0] # see how many counters light would have if it made this move
                if light_counters > best_score:
                    best_score = light_counters
                    best_move = (i, j)
    return best_move

@app.route('/')
def initialise_flask():
    global board, counter
    counter = 60    # we initialise counter again here in case the user restarts
    board = components.initialise_board()
    return render_template('index.html', game_board=board)

@app.route('/move')
def get_move():
    global board, counter
    print(counter)
    colour = 'Dark '    # dark goes first
    if move_is_available('Dark ', board) == False and move_is_available('Light', board) == False:
        result = game_over(board)
        print(result)
    try:
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        coords = (x, y)
    except (TypeError, ValueError):
        # return an error if coordinates are missing or invalid
        return jsonify({'status': 'fail', 'message': 'Invalid coordinates received.'})
    if components.legal_move(colour, coords, board) is False:
        return jsonify({'status': 'fail', 'message': "This is not a legal move. Select different coordinates."})
    board = swap_colours(colour, coords, board)
    # we check again that the move is available because if the board is full then the 
    # /move route cannot be called again, so there is no way to check the board is full
    # after the final counter has been placed, unless we do it at the end of this function
    if move_is_available('Dark ', board) == False and move_is_available('Light', board) == False:
        result = game_over(board)
        print(result)
    board = swap_colours('Light', ai(board), board)
    counter -= 2
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
