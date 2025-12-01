def cli_coords_input():
	x, y = 9, 9
	while not (1<=x<=8 and 1<=y<=8):
		try:
			x = int(input("Input your x coordinate: "))
			assert 1<=x<=8
			y = int(input("Input your y coordinate: "))
			assert 1<=y<=8
		except (ValueError, AssertionError):
			print("You must enter a number between 1 and 8")
	coords = (x, y)
	print(coords)

cli_coords_input()
