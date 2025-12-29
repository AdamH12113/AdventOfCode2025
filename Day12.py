import re, sys, copy
from collections import namedtuple

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

# Process the input. It's a sequence of six 2D diagrams of present shapes followed by a list of
# storage spaces and quantities of those presents.
Area = namedtuple('Area', ['x', 'y', 'shape_counts'])

groups = input_text.split('\n\n')
shapes = []
for st in groups[:6]:
	shapes.append(st.split('\n')[1:])
areas = []
for at in groups[6].split('\n'):
	halves = at.split(': ')
	dims = halves[0].split('x')
	counts = [int(n) for n in halves[1].split(' ')]
	areas.append(Area(int(dims[0]), int(dims[1]), counts))

# Part 1: How many regions can fit all of the listed presents? This is something like an NP-hard
# problem in general, but apparently (from discussion online) a very simple area-based heuristic
# works perfectly. What a weird puzzle!
flattened_shapes = [''.join(''.join(line for line in shape)) for shape in shapes]
shape_areas = [sum(1 for c in shape if c == '#') for shape in flattened_shapes]

num_fits = 0
for area in areas:
	needed_area = sum(area.shape_counts[s]*shape_areas[s] for s in range(6))
	actual_area = area.x * area.y
	if actual_area >= needed_area:
		num_fits += 1
print(f"Part 1: The number of regions that can fit all the presents is: {num_fits}")
