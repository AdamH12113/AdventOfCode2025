import re, sys, copy
from Vector import Vector, up, down, left, right, upleft, upright, downleft, downright

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{e.__class__.__name__}] {e}")
	exit()

# Process the input. It's a 2D grid consisting of empty spaces ('.'), splitters ('^'), and a start
# point ('S'). I'm going to reverse the Y coordinates to make the code easier to follow.
rows = list(reversed(input_text.split('\n')))
ysize = len(rows)
xsize = len(rows[0])
start_grid = {}
for y in range(ysize):
	for x in range(xsize):
		if rows[y][x] == '^':
			start_grid[Vector(x, y)] = '^'
		else:
			start_grid[Vector(x, y)] = '.'
		if rows[y][x] == 'S':
			start = Vector(x, y)

# Part 1: How many times is a beam split? The only tricky part is that beams in the same space
# combine into a single beam, so we have to avoid double-counting.
def propagate_beam(loc: Vector, grid: dict) -> bool:
	if loc + down not in grid:
		return False
	if grid[loc + down] == '.':
		grid[loc + down] = '|'
		return False
	elif grid[loc + down] == '^':
		grid[loc + downleft] = '|'
		grid[loc + downright] = '|'
		return True
	else:
		return False

grid = copy.deepcopy(start_grid)
propagate_beam(start, grid)
num_splits = 0
for y in range(ysize - 2, 0 - 1, -1):
	for x in range(xsize):
		loc = Vector(x, y)
		if grid[loc] == '|':
			num_splits += propagate_beam(loc, grid)
print(f"Part 1: The number of beam splits is: {num_splits}")

# Part 2: Now we're doing wave-particle duality and we need to know how many possible paths there
# are for a single particle taking each possible split from each splitter. Time for a recursive DFS!
# That takes a long time, so we'll have to add memorization.
cache = {}
def propagate_particle(loc: Vector, grid: dict) -> int:
	if loc in cache:
		return cache[loc]

	if loc + down not in grid:
		num = 1
	elif grid[loc + down] == '.':
		num = propagate_particle(loc + down, grid)
	else:
		num = propagate_particle(loc + downleft, grid) + propagate_particle(loc + downright, grid)
	cache[loc] = num
	return num

grid = copy.deepcopy(start_grid)
num_paths = propagate_particle(start, grid)
print(f"Part 2: The number of timelines is: {num_paths}")
