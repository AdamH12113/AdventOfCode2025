import re, sys, copy, networkx
from Vector import Vector

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

# Process the input. It's a list of coordinates giving the location of red tiles on a tile floor.
red_tiles = [Vector(*[int(c) for c in coords.split(',')]) for coords in input_text.split('\n')]

# Part 1: What is the largest-area rectangle that can be made using two red tiles as opposite corners?
max_area = 0
for t1 in range(len(red_tiles)):
	for t2 in range(t1+1, len(red_tiles)):
		dist = red_tiles[t1] - red_tiles[t2]
		area = (abs(dist.x)+1) * (abs(dist.y)+1)
		if area > max_area:
			max_area = area
print(f"Part 1: The largest possible area is: {max_area}")

# Part 2: The red tiles now form the corners of a solid region filled with green tiles. The largest
# rectangle must have red tiles in opposite corners but the rectangle itself must only be composed
# of red and green tiles. How big is the largest possible rectangle now?


