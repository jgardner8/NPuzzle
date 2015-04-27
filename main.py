"""
This program only supports python 3.
"""

from sys import argv
from os import path
from search_strategies import strategy_by_name
import time

def parse_args():
	assert len(argv) == 3, "Must be called in form: search filename method"
	filename, method = argv[1], argv[2]
	return filename, method

def puzzle_from_file(filename):
	"""
	Converts a puzzle file into type ([][], [][]), where the first element of the tuple is the 
	  initial_state and the second is the desired_state.
	Example file:
	2x3          | width x height
	1 2 3 4 0 5  | initial_state
	3 1 2 4 5 0  | desired_state
	"""
	def state_from_line(line):
		"""
		Converts a single line of a puzzle file that represents a state into a 2d array.
		Example: "1 2 3 4 0 5" is converted into [[1,2],[3,4],[0,5]] if puzzle dimensions are 2x3
		"""
		state = [[] for x in range(width)]
		for x in range(width):
			for y in range(height):
				state[x].append(line[x + y*width])
		return state

	assert path.isfile(filename), "File '" + filename + "' does not exist!"
	with open(filename) as file:
		contents = file.read().split('\n')
		dimensions = contents[0].split('x')
		width, height = int(dimensions[0]), int(dimensions[1])
		initial_state = state_from_line(contents[1].split(' '))
		desired_state = state_from_line(contents[2].split(' '))
		return initial_state, desired_state

def _main():
	filename, method = parse_args()
	initial_state, desired_state = puzzle_from_file(filename)
	
	start_time = time.process_time() # does not include time process was swapped out
	number_of_nodes, solution = strategy_by_name(method)(initial_state, desired_state)
	print("Time taken: " + str(time.process_time() - start_time) + " secs")
	
	print(filename, method, number_of_nodes)
	if solution != None:
		for action in solution: 
			print(action, end='')
	else:
		print("No solution found.")

if __name__ == "__main__":
	_main()
