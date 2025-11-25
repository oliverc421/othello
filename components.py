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

def legal_move(colour: str, coordinate: tuple, board: list) -> bool
	if board[coordinate[0]][coordinate[1]] != 'None ':
		return False	
	if colour == 'Light ':
		opponent = 'Dark '
	else:
		opponent = 'Light ' 

	for i in range (-1, 2):			# checking all the squares around the selected square
		for j in range (-1,2):
			try:
				if board[(coordinate[0]+i)][(coordinate[1]+j)] == opponent:	# i want to capture this direction to check if there is a same colour counter further down
					for k in range (2,8):
						try:
							if board[(coordinate[0]+k*i)][(coordinate[1]+k*j)] == colour: # timesing k by i and j means it goes in the 														specfic direction it needs to, if the target counter is 													to the left (coordinate(0) - 1) then continuing to minus 														is what i want to do
								return True
						except: 
							break
					except:
						pass
			
