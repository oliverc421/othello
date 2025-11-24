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

def print_board():
	print(initialise_board())	

def legal_move(colour: str, coordinate: tuple, board: object) -> bool
	
