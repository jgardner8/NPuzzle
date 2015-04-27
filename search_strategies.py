"""
Defines multiple strategies to solve the puzzle. Each has different advantages/disadvantages 
	discussed in the included report.
The search strategies return the number of nodes still in the open set and the solution as a tuple
Terminology used:
* Open set: The set of nodes that need to be searched (aka frontier).
* Closed set: The set of nodes that have already been searched, and don't need to be 
		reconsidered. Avoids loops and improves performance.
* Action: A valid move in the puzzle. See actions.py
* Successor: The state that immediately follows the current state after taking an action.
* Heuristic: See heuristics.py 
"""
from actions import up, down, left, right
from collections import deque
from bisect import bisect_left, insort
from queue import PriorityQueue, Empty
import heuristics

class Node(object): # pylint: disable=too-few-public-methods
	def __init__(self, state, parent, action_taken):
		self.state = state
		self.parent = parent
		self.action_taken = action_taken
		self.num_parents = 0 if parent == None else parent.num_parents + 1

	# ordering does not matter, needed for use in priority queue when priorities are equal
	def __lt__(self, other): return False 

def _bisect_index(collection, value):
	"""
	Searches collection for value using binary search, returning the index of value or None.
	collection _must_ be sorted!
	"""
	i = bisect_left(collection, value)
	if i != len(collection) and collection[i] == value:
		return i
	return None

def _state_is_valid(state, closed_set):
	return (state != None and 
			_bisect_index(closed_set, state) == None)

def _search(initial_state, desired_state, open_set_get, open_set_add):
	"""
	Avoids repetition of the generic parts of all of the search strategies. 
	The search strategies turn out to be similar except in the way the open set data structure works. 
	open_set_get: () -> Node. Pulls the next relevant node from the open set.
	open_set_add: Node -> (). Adds a successor node to the open set.
	reverse_add_calls: Adds successors to open_set in order right, down, left, up instead of up, left, down, right.
	"""
	def open_set_add_if_new(successor_state, action_taken):
		if _state_is_valid(successor_state, closed_set):
			open_set_add(Node(successor_state, current_node, action_taken))

	def reconstruct_actions(node):
		actions = []
		while node.action_taken != None:
			actions.append(node.action_taken)
			node = node.parent
		return actions

	closed_set = []
	current_node = Node(initial_state, None, None)
	while current_node.state != desired_state:
		insort(closed_set, current_node.state) # adds state to closed_set while maintaining sorted order.
		
		open_set_add_if_new(up(current_node.state), "Up;")
		open_set_add_if_new(left(current_node.state), "Left;")
		open_set_add_if_new(down(current_node.state), "Down;")
		open_set_add_if_new(right(current_node.state), "Right;")

		try:
			current_node = open_set_get()
		except (IndexError, Empty):
			return len(closed_set), None

	return len(closed_set), reconstruct_actions(current_node)

def depth_first(initial_state, desired_state):
	"""
	Select an option and continue with it until no more valid actions exist.
	Then backtrack until one or more actions become valid.
	Complete because puzzle has no infinite paths and closed_set stops loops, non-optimal, very slow for 
		this puzzle.
	"""
	open_set = [] # stack that contains Nodes
	return _search(initial_state, desired_state, 
		open_set_get=open_set.pop, open_set_add=open_set.append)

def breadth_first(initial_state, desired_state):
	"""
	Perform every possible action one level at a time, pursuing all possible solutions equally. 
	Complete, optimal because all actions have equal cost, slow for this puzzle.
	"""
	open_set = deque() # queue that contains Nodes
	return _search(initial_state, desired_state, 
		open_set_get=open_set.popleft, open_set_add=open_set.append)
	
def greedy_best_first(initial_state, desired_state, heuristic=heuristics.manhattan_distance):
	"""
	Like depth-first, except chooses the option to pursue based on a heuristic rather than a pre-defined order. 
	Complete because puzzle has no infinite paths and closed_set stops loops, non-optimal, fast for this puzzle.
	"""
	def open_set_add(node):
		priority = heuristic(node.state, desired_state)
		open_set.put( (priority, node) )

	def open_set_get():
		_, node = open_set.get_nowait()
		return node

	open_set = PriorityQueue() # contains (priority, Node)
	return _search(initial_state, desired_state, open_set_get, open_set_add)
	
def a_star(initial_state, desired_state, heuristic=heuristics.manhattan_distance):
	"""
	Like greedy best-first, except considers the cost already incurred to reach the current state in addition
	  to the value of the heuristic.
	This results in interesting behaviour where promising paths can be pursued relentlessly like 
		depth-first search, but when paths appear similar each of them are considered. 
	Complete, optimal because heuristic is monotone, very fast (fastest informed) for this puzzle.
	"""
	def open_set_add(node):
		priority = node.num_parents + heuristic(node.state, desired_state)
		open_set.put( (priority, node) )

	def open_set_get():
		_, node = open_set.get_nowait()
		return node

	open_set = PriorityQueue() # contains (priority, Node)
	return _search(initial_state, desired_state, open_set_get, open_set_add)

def dijkstra(initial_state, desired_state):
	"""
	Like breadth-first search in spirit, except expands nodes with the least cost incurred so far
		first rather than nodes with the least parents first. As all actions have equal cost in this 
		puzzle, it is equivalent to breadth-first search, but may expand nodes slightly differently 
		due to how the PriorityQueue data structure sorts nodes of equal priority. 
	It is equivalent to A* with a heuristic of 0 in all cases.
	Complete, optimal, slow for this puzzle.
	"""
	return a_star(initial_state, desired_state, heuristic=lambda current_state, desired_state: 0)

def depth_limited(initial_state, desired_state):
	"""
	Depth-limited search where max depth is increased if solution is not found.
	Performs a depth-first search limited to max_depth. Once all nodes are expanded max_depth is increased.
	Lower max_depth values can increase likelihood of optimal solution. Around 3 seems fastest for this puzzle.
	Complete because puzzle has no infinite paths and closed_set stops loops, non-optimal if max_depth > 1, 
		average speed (fastest uninformed) for this puzzle.
	"""
	def open_set_add(node):
		if node.num_parents < max_depth*iteration:
			open_set.append(node)
		else:
			paused_set.append(node)

	def open_set_get():
		nonlocal open_set, paused_set, iteration
		if len(open_set) == 0:
			open_set = paused_set
			paused_set = []
			iteration += 1 # pylint: disable=unused-variable
		return open_set.pop()

	open_set = [] # stack that contains Nodes
	paused_set = [] # contains nodes that can't be pursued yet because they exceed max_depth
	max_depth = 3 # configurable (see docstring)
	iteration = 1
	return _search(initial_state, desired_state, open_set_get, open_set_add)
	
def hill_climb(initial_state, desired_state, heuristic=heuristics.manhattan_distance):
	"""
	Hill climb search with configurable amount of backtracking allowed. 
	Similar to A*, but tries to restrict backtracking to severely worse states under the naive belief that this
		puzzle, as opposed to most of the pathfinding that A* is typically used for, doesn't involve much backtracking.
	Besides the fact that the puzzle does involve more backtracking than assumed, adding worse states to the 
		priority queue seems to cost very little as they're unlikely to ever be expanded anyway. The advantage
		of the shorter queue when keeping sorted order appears to have minimal impact.
	The fact that it's a hill climb search means it suffers from the same local maximum problems that all hill 
		climb searches suffer from unless backtracking_allowed is sufficiently high. In practice this doesn't help 
		because if backtracking_allowed is >= 3 and the manhattan_distance heuristic is used, the algorithm is 
		equivalent to A* anyway. This is because in one action the manhattan_distance can only increase by up to 2 
		in this puzzle and the number of actions taken can of course only increase by 1.
	Incomplete if backtracking_allowed < 3 when manhattan_distance heuristic is used, non-optimal, 
		fast (but slower than A* which it was based upon) for this puzzle.
	"""
	def open_set_add(node):
		if node.num_parents > 0:
			parent_priority = node.num_parents-1 + heuristic(node.parent.state, desired_state)
			current_priority = node.num_parents + heuristic(node.state, desired_state)
			if current_priority > parent_priority + backtracking_allowed:
				return
		open_set.put( (current_priority, node) )

	def open_set_get():
		_, node = open_set.get_nowait()
		return node

	backtracking_allowed = 2 # any movement that increases the heuristic more than this is not considered
	open_set = PriorityQueue() # contains (priority, Node)
	return _search(initial_state, desired_state, open_set_get, open_set_add)

def strategy_by_name(name):
	"""
	Returns the search strategy function that is named by the string parameter.
	"""
	def available_strategies():
		return ( 
			str(
				sorted(list(methods.keys())) # sorted list of keys
			)[1:-1] # remove square brackets from start and end
		).replace('\'', '') # remove quotes around strings

	methods = {
		'DFS': depth_first,
		'BFS': breadth_first,
		'GBFS': greedy_best_first,
		'AS': a_star,
		'DIJ': dijkstra,
		'DL': depth_limited,
		'HC': hill_climb
	}
	assert name in methods, "Search strategy '" + name + "' is not implemented. Available: " + available_strategies()
	return methods[name.upper()]
