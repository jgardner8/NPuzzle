"""
Defines all the actions one can take to solve the puzzle
Each action returns None when resulting state is invalid, otherwise returns a _new_ state
"""

from copy import deepcopy
from helpers import coords_of_tile

def _move(state, tile_to_swap):
	"""
	A generic way of moving the empty tile around. 
	Returns None when resulting state is invalid, otherwise returns a _new_ state.
	tile_to_swap: (int, int) representing an offset from the position of the empty tile. 
	"""
	assert state != None, "Can't move from null state."
	assert tile_to_swap[0] == 0 or tile_to_swap[1] == 0, "Can't move diagonally."
	assert abs(tile_to_swap[0]) == 1 or abs(tile_to_swap[1]) == 1, "Can't move more than one space."

	x, y = coords_of_tile(state, '0')
	x2, y2 = x + tile_to_swap[0], y + tile_to_swap[1]
	if x2 not in range(len(state)) or y2 not in range(len(state[0])): 
		return None
	new_state = deepcopy(state)
	new_state[x][y], new_state[x2][y2] = new_state[x2][y2], new_state[x][y]
	return new_state

def up(state):
	return _move(state, (0, -1))

def left(state):
	return _move(state, (-1, 0))

def down(state):
	return _move(state, (0, 1))

def right(state):
	return _move(state, (1, 0))
