"""
Heuristics estimate cost of the cheapest path from current_state to desired_state to inform search strategies.
Each of these are "admissable" - they never overestimate the cost.
Each of these are also "consistent" or "monotone" - the value of the heuristic for a given state is less than
	or equal to the heuristic for the state's neighbour plus the cost to reach that neighbour. 
"""

from helpers import coords_of_tile

def number_of_misplaced_tiles(current_state, desired_state):
	"""
	Counts the number of tiles in current_state that aren't in the same position as desired_state.
	"""
	misplaced = 0
	for x, column in enumerate(current_state):
		for y, tile in enumerate(column):
			if tile != desired_state[x][y]:
				misplaced += 1
	return misplaced

def manhattan_distance(current_state, desired_state):
	"""
	Calculates distance of every tile in current_state to its position in desired_state and sums them.
	"""
	total_distance = 0
	for column in current_state:
		for tile in column:
			current_coords, desired_coords = coords_of_tile(current_state, tile), coords_of_tile(desired_state, tile)
			total_distance += abs(current_coords[0] - desired_coords[0]) + abs(current_coords[1] - desired_coords[1])
	return total_distance
	