#### Description
The [N-Puzzle](https://en.wikipedia.org/wiki/N-puzzle) is known by many names such as 8-puzzle, 15-puzzle, sliding tile puzzle etc. It is a puzzle where `n` tiles are placed in a grid of `n+1` spaces, leaving one empty space. The tiles must be moved into sequential order by sliding tiles into the empty space. Some variations use an image that must be un-shuffled; the variation considered here has numbered tiles. 

There is no known algorithm to solve the N-Puzzle, so we must use a brute-force technique to find a solution. As a puzzle with `n` tiles has `(n+1)! / 2` possible states [1] and finding the shortest possible solution to any given N-Puzzle has been proven to be NP-complete [1], the brute-force technique must be informed in order to solve larger puzzles. 

A selection of tree-based search algorithms have been implemented to solve the N-Puzzle. Some are more efficient than others, but all will eventually fail when given a large enough puzzle due to memory or time constraints. Some of the algorithms are complete and/or optimal, some are not. See `search_strategies.py` for more information about this.

Currently implemented: 
* Depth-first search
* Breadth-first search
* Greedy best-first search
* A*
* Dijkstra's algorithm
* Depth-limited search
* Hill-climb search

#### Build/Run
The program can be run in a Python 3 interpreter. Python 2 is not supported. It is not necessary to build the program befre running it, although you can if you'd like to run it on a machine without Python.  
Run: `python main.py puzzles/7x7.txt AS`  
Build: `python setup.py build`

Returns the time taken to find a solution, the name of the puzzle, the search method used, the number of nodes searched and finally the solution. The solution is in respect to the empty tile, so when it says _Down_ for example, you must swap the empty tile with the tile below it. 