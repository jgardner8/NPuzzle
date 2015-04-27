"""
Helpful functions that don't fit into a particular category. 
"""

def coords_of_tile(state, tile_to_find):
	"""
	Returns (int, int) representing coordinates of tile_to_find in state
	"""
	for x, column in enumerate(state):
		for y, tile in enumerate(column):
			if tile == tile_to_find:
				return x, y
	raise ValueError("tile " + str(tile_to_find) + " does not exist in state " + str(state))
	