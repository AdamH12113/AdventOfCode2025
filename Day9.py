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
# After seeing part 2 I'm revising part 1 to find all possible rectangle sizes and sort them.
rect_sizes = []
for t1 in range(len(red_tiles)):
	for t2 in range(t1+1, len(red_tiles)):
		dist = red_tiles[t1] - red_tiles[t2]
		area = (abs(dist.x)+1) * (abs(dist.y)+1)
		rect_sizes.append((red_tiles[t1], red_tiles[t2], area))
rect_sizes.sort(key = lambda t: t[2], reverse = True)
print(f"Part 1: The largest possible area is: {rect_sizes[0][2]} {rect_sizes[0][0]} {rect_sizes[0][1]}")

# Part 2: The red tiles now form the corners of a solid region filled with green tiles. The largest
# rectangle must have red tiles in opposite corners but the rectangle itself must only be composed
# of red and green tiles. How big is the largest possible rectangle now? I know I've done this sort
# of thing in a previous AoC. It's a bit convoluted, so starting from a sorted list of the largest
# rectangles will help.

# This is tricky. The rectangle will partially overlap with the border of the polygon, so a simple
# containment isn't quite what I'm looking for. Maybe walking around the edge of the polygon looking
# for line crossings would work? How do I even tell which side is the inside of the polygon just
# from looking at the coordinates? Hmm... okay, the rectangle is going to overlap the interior of
# the polygon no matter what, right? No, it's not. Argh. I think I'm going to have to find an
# algorithm online.
def line_in_polygon(x1: int, x2: int, y1: int, y2: int, polygon: list[Vector]) -> bool:
	# Give all coordinate pairs the same orientation
	if x1 > x2:
		x2, x1 = x1, x2
	if y1 > y2:
		y2, y1 = y1, y2
	
	for t1 in range(len(polygon)):
		t2 = (t1 + 1) % len(polygon)
		px1 = polygon[t1].x
		px2 = polygon[t2].x
		py1 = polygon[t1].y
		py2 = polygon[t2].y
		
print(min(v.x for v in red_tiles))
print(max(v.x for v in red_tiles))
print(min(v.y for v in red_tiles))
print(max(v.y for v in red_tiles))



