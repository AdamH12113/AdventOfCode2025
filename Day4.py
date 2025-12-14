import re, sys, copy
from Vector import Vector, up, down, left, right, upleft, upright, downleft, downright, null

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

# Process the input. It's a 2D square grid showing rolls of paper ('@') and empty spaces ('.'). In
# anticipation of whatever part 2 will ask us to do, let's use a sparse representation with a set.
grid_text = input_text.split('\n')
grid_size = len(grid_text)
start_grid = set() 
for y in range(0, grid_size):
	for x in range(0, grid_size):
		if grid_text[y][x] == '@':
			start_grid.add(Vector(x, y))

# Part 1: How many rolls of paper are accessible? An accessible roll has fewer than four rolls of
# paper in the eight adjacent positions.
def count_adjacent_rolls(grid: set, v: Vector) -> int:
	return (v + upleft in grid) + (v + up in grid) + (v + upright in grid) + \
	       (v + left in grid) +                           (v + right in grid) + \
	       (v + downleft in grid) + (v + down in grid) + (v + downright in grid)

accessible_rolls = sum(count_adjacent_rolls(start_grid, v) < 4 for v in start_grid)
print(f"Part 1: The number of accessible rolls is: {accessible_rolls}")

# Part 2: How many rolls of paper can be removed? Any accessible roll can be removed, and removing
# a roll may cause other rolls to become accessible. There's probably a fancy recursive solution,
# but a simple iterative solution will suffice.
removed_rolls = 0
roll_removed_this_iteration = True
grid = copy.deepcopy(start_grid)

# Since we're updating the set as we go, we need to make a copy of the values to iterate over
while roll_removed_this_iteration:
	roll_removed_this_iteration = False
	for roll in list(grid):
		if count_adjacent_rolls(grid, roll) < 4:
			grid.remove(roll)
			removed_rolls += 1
			roll_removed_this_iteration = True
print(f"Part 2: The number of rolls removed was: {removed_rolls}")
