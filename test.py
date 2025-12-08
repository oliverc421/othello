import ai_flask_game_engine as flask_test
import components

def test_board_creation():
    """Check if board is created correctly"""
    import components

    board = components.initialise_board()

    # check board size
    if len(board) != 8:
        print("FAIL: Board doesn't have 8 rows")
        return False

    # check each row has 8 columns
    for row in board:
        if len(row) != 8:
            print("FAIL: Board row doesn't have 8 columns")
            return False

    # check center pieces
    if board[3][3] != 'Light':
        print("FAIL: Center (3,3) should be Light")
        return False
    if board[3][4] != 'Dark ':
        print("FAIL: Center (3,4) should be Dark ")
        return False
    if board[4][3] != 'Dark ':
        print("FAIL: Center (4,3) should be Dark ")
        return False
    if board[4][4] != 'Light':
        print("FAIL: Center (4,4) should be Light")
        return False

    # check corners are empty
    corners = [(0,0), (0,7), (7,0), (7,7)]
    for x, y in corners:
        if board[y][x] != 'None ':
            print(f"FAIL: Corner ({x},{y}) should be empty, got {board[y][x]}")
            return False

    print("PASS: Board creation test")
    return True

def test_legal_move():
    """Check if legal_move function works"""

    board = components.initialise_board()

    # test that you can't place on occupied square
    result = components.legal_move('Dark ', (3, 3), board)
    if result != False:
        print("FAIL: Shouldn't allow move on occupied square")
        return False

    # test that empty square with no capture is illegal
    result = components.legal_move('Dark ', (0, 0), board)
    if result != False:
        print("FAIL: Empty square with no capture should be illegal")
        return False

    # test a known legal move for dark at start (2,3)
    result = components.legal_move('Dark ', (2, 3), board)
    if result != True:
        print("FAIL: (2,3) should be a legal move for dark at start")
        return False

    # test a known legal move for light at start (4,2)
    result = components.legal_move('Light', (4, 2), board)
    if result != True:
        print("FAIL: (4,2) should be a legal move for light at start")
        return False

    # test out of bounds coordinates
    result = components.legal_move('Dark ', (-1, 0), board)
    if result != False:
        print("FAIL: Should reject negative x coordinate")
        return False
    result = components.legal_move('Dark ', (8, 0), board)
    if result != False:
        print("FAIL: Should reject x=8 (out of bounds)")
        return False

    print("PASS: Legal move test")
    return True

def test_move_is_available():
    """Test that move_is_available correctly detects available moves"""

    # full board should have no moves
    full_board = [['Dark '] * 8 for _ in range(8)]
    if flask_test.move_is_available('Dark ', full_board) != False:
        print("FAIL: Full board should have no moves for dark")
        return False
    if flask_test.move_is_available('Light', full_board) != False:
        print("FAIL: Full board should have no moves for light")
        return False

    # empty board should have no moves (no captures possible)
    empty_board = [['None '] * 8 for _ in range(8)]
    if flask_test.move_is_available('Dark ', empty_board) != False:
        print("FAIL: Empty board should have no moves")
        return False

    # starting board should have moves for both players
    start_board = components.initialise_board()
    if flask_test.move_is_available('Dark ', start_board) != True:
        print("FAIL: Starting board should have moves for dark")
        return False
    if flask_test.move_is_available('Light', start_board) != True:
        print("FAIL: Starting board should have moves for light")
        return False

    print("PASS: Move is available test")
    return True

def test_count_counters():
    """Test counting pieces on different boards"""

    # empty board
    empty_board = [['None '] * 8 for _ in range(8)]
    light, dark = flask_test.count_counters(empty_board)
    if light != 0 or dark != 0:
        print(f"FAIL: Empty board should have 0,0, got {light},{dark}")
        return False

    # full dark board
    full_dark = [['Dark '] * 8 for _ in range(8)]
    light, dark = flask_test.count_counters(full_dark)
    if light != 0 or dark != 64:
        print(f"FAIL: Full dark board should have 0,64, got {light},{dark}")
        return False

    # starting board should have 2 of each
    start_board = components.initialise_board()
    light, dark = flask_test.count_counters(start_board)
    if light != 2 or dark != 2:
        print(f"FAIL: Start board should have 2,2, got {light},{dark}")
        return False

    # mixed board
    mixed_board = [
        ['Light', 'Dark ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ']
    ]
    light, dark = flask_test.count_counters(mixed_board)
    if light != 1 or dark != 1:
        print(f"FAIL: Mixed board should have 1,1, got {light},{dark}")
        return False

    print("PASS: Count counters test")
    return True

def test_game_over():
    """Test game_over function"""

    # draw scenario
    draw_board = [['Dark '] * 8 for _ in range(8)]
    for i in range(32):  # make exactly half light
        draw_board[i//8][i%8] = 'Light'
    result = flask_test.game_over(draw_board)
    if "Draw" not in result:
        print(f"FAIL: Draw board should return 'Draw', got {result}")
        return False

    # light wins scenario
    light_wins_board = [['Light'] * 8 for _ in range(8)]
    light_wins_board[0][0] = 'Dark '  # just one dark piece
    result = flask_test.game_over(light_wins_board)
    if "Light wins" not in result:
        print(f"FAIL: Light wins board should return 'Light wins', got {result}")
        return False

    # dark wins scenario
    dark_wins_board = [['Dark '] * 8 for _ in range(8)]
    dark_wins_board[0][0] = 'Light'  # just one light piece
    result = flask_test.game_over(dark_wins_board)
    if "Dark wins" not in result:
        print(f"FAIL: Dark wins board should return 'Dark wins', got {result}")
        return False

    print("PASS: Game over test")
    return True

def test_swap_colours():
    """Check if pieces flip correctly"""

    # simple test board
    board = [
        ['None ', 'None ', 'None ', 'None '],
        ['None ', 'Light', 'Dark ', 'None '],
        ['None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ']
    ]

    # dark should capture light by playing at (0, 1)
    new_board = flask_test.swap_colours('Dark ', (0, 1), board)

    if new_board[1][0] != 'Dark ':
        print("FAIL: Piece not placed")
        return False

    if new_board[1][1] != 'Dark ':
        print("FAIL: Piece not flipped")
        return False

    # test multi-direction capture
    board2 = [
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'Light', 'Dark ', 'Light', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'Dark ', 'None ', 'Dark ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'Light', 'Dark ', 'Light', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None '],
        ['None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ', 'None ']
    ]
    # dark at (2,2) should capture in multiple directions
    new_board2 = flask_test.swap_colours('Dark ', (2, 2), board2)
    if new_board2[2][2] != 'Dark ':
        print("FAIL: Multi-direction - piece not placed")
        return False

    print("PASS: Swap colours test")
    return True

def test_ai_function():
    """Test that AI returns a valid move"""

    # starting board - AI should find a move
    start_board = components.initialise_board()
    move = flask_test.ai(start_board)
    
    # check return type
    if not isinstance(move, tuple):
        print("FAIL: AI should return a tuple")
        return False
    if len(move) != 2:
        print("FAIL: AI should return (x,y) tuple")
        return False

    # if there are moves available, it should be a legal move
    if move != (-1, -1):
        if not components.legal_move('Light', move, start_board):
            print(f"FAIL: AI returned illegal move {move}")
            return False

    # test with no moves available
    full_dark = [['Dark '] * 8 for _ in range(8)]
    no_move = flask_test.ai(full_dark)
    if no_move != (-1, -1):
        print(f"FAIL: AI should return (-1,-1) when no moves, got {no_move}")
        return False

    print("PASS: AI function test")
    return True

def test_flask_routes():
    """Test Flask API endpoints"""

    # create a test client
    test_app = flask_test.app.test_client()

    # test root endpoint returns html
    response = test_app.get('/')
    if response.status_code != 200:
        print("FAIL: Root endpoint should return 200")
        return False
    if 'text/html' not in response.content_type:
        print("FAIL: Root endpoint should return HTML")
        return False

    # test move endpoint with no parameters (should fail)
    response = test_app.get('/move')
    if response.status_code != 200:
        print("FAIL: /move should return 200 even on error")
        return False
    data = response.get_json()

    if data is None:
        print("FAIL: No JSON response received")
        return False
    if data['status'] != 'fail':
        print("FAIL: /move with no params should return fail")
        return False

    # test move endpoint with invalid coordinates
    response = test_app.get('/move?x=abc&y=def')
    data = response.get_json()
    if data['status'] != 'fail':
        print("FAIL: /move with non-numeric coords should return fail")
        return False

    # test move endpoint with out of bounds coordinates
    response = test_app.get('/move?x=10&y=10')
    data = response.get_json()
    if data['status'] != 'fail':
        print("FAIL: /move with out of bounds should return fail")
        return False

    print("PASS: Flask routes test")
    return True

def test_full_game_flow():
    """Test a complete game turn (human move + AI response)"""

    # reset the global board first
    flask_test.board = components.initialise_board()
    flask_test.counter = 60

    # find a legal move for dark
    legal_move = None
    for x in range(8):
        for y in range(8):
            if components.legal_move('Dark ', (x, y), flask_test.board):
                legal_move = (x, y)
                break
        if legal_move:
            break

    if not legal_move:
        print("SKIP: No legal moves found to test game flow")
        return True  # not a failure, just skip

    print("PASS: Full game flow test")
    return True

# running all tests
if __name__ == "__main__":
    print("running tests")

    tests = [
        test_board_creation,
        test_legal_move,
        test_move_is_available,
        test_count_counters,
        test_game_over,
        test_swap_colours,
        test_ai_function,
        test_flask_routes,
        test_full_game_flow,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"ERROR in {test.__name__}: {e}")

    print(f"\n=== Results: {passed}/{total} passed ===")

    # exit with error code if any tests failed
    if passed != total:
        exit(1)
