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

def legal_move(colour: str, coordinate: tuple, board: list) -> bool:
	x, y = coordinate
	if board[x][y] != 'None ':
		print("There is already a counter on this square. Select different coordinates")
		return False	
	if colour == 'Light':
		opponent = 'Dark '
	else:
		opponent = 'Light' 

	for i in range (-1, 2):			# checking all the squares around the selected square
		for j in range (-1,2):
			try:
				if board[(x+i)][(y+j)] == opponent:	# i want to capture this direction to check if there is 														a same colour counter further down
					for k in range (1,8):
						try:
							if board[(x+k*i)][(y+k*j)] != opponent: # timesing k by i and j means it goes in the 														specfic direction it needs to, if the target counter is 													to the left (coordinate(0) - 1) then continuing to minus 														is what i want to do
								if board[(x+k*i)][(y+k*j)] == 'None ':	# if we hit a blank square, exit the nested loop and check the other squares
									break
								else:
									return True
						except: 
							break
			except:
				pass
	print("This is not a legal move. Select different coordinates.")			
