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
minx = min(t.x for t in red_tiles)
maxx = max(t.x for t in red_tiles)
miny = min(t.y for t in red_tiles)
maxy = max(t.y for t in red_tiles)

# Part 1: What is the largest-area rectangle that can be made using two red tiles as opposite corners?
# After seeing part 2 I'm revising part 1 to find all possible rectangle sizes and sort them.
rect_sizes = []
for t1 in range(len(red_tiles)):
	for t2 in range(t1+1, len(red_tiles)):
		dist = red_tiles[t1] - red_tiles[t2]
		area = (abs(dist.x)+1) * (abs(dist.y)+1)
		rect_sizes.append((red_tiles[t1], red_tiles[t2], area))
rect_sizes.sort(key = lambda t: t[2], reverse = True)
print(f"Part 1: The largest possible area is: {rect_sizes[0][2]}")

# Part 2: The red tiles now form the corners of a solid region filled with green tiles. The largest
# rectangle must have red tiles in opposite corners but the rectangle itself must only be composed
# of red and green tiles. How big is the largest possible rectangle now? I know I've done this sort
# of thing in a previous AoC. It's a bit convoluted, so starting from a sorted list of the largest
# rectangles will help.

# This is tricky. The rectangle will partially overlap with the border of the polygon, so a simple
# containment isn't quite what I'm looking for. Maybe walking around the edge of the polygon looking
# for line crossings would work? How do I even tell which side is the inside of the polygon just
# from looking at the coordinates? Hmm... okay, the rectangle is going to overlap the interior of
# the polygon no matter what, right? No, it's not. Argh.

# Okay, let's think this through. If the rectangle's border lines are all inside the polygon, then
# the interior must be in the polygon too. So what cases do we have to deal with for those lines?
#   1. The line is within a polygon border segment.
#      a. The line contains both red tile endpoints of the border segment.
#      b. The line contains one red tile endpoint.
#      c. The line contains neither red tile endpoint.
#   2. The line partially overlaps a polygon border segment.
#      a. The non-overlapping part of the line is inside the polygon.
#      b. The non-overlapping part of the line is outside the polygon.
#   3. The line partially overlaps multiple polygon border segments.
#      a. The non-overlapping part(s) are inside the polygon.
#      b. At least one non-overlapping part is outside the polygon.
#   4. The line is entirely within the polygon.
#   5. The line is entirely outside the polygon.
#   6. The line crosses the polygon border.
# The tricky part is the corners. I can find out whether a line is entirely contained within the
# polygon easily by projecting the line outward and counting how many times it crosses the polygon
# boundary. But when a line crosses a boundary corner, how do I know whether it's staying within
# the polygon or going outside of it?

# While trying to find polygon-clipping algorithms, I ran across this, which gave me an idea:
#   https://sites.cc.gatech.edu/grads/h/Hao-wei.Hsieh/Haowei.Hsieh/mm.html#sec3
# What if, instead of checking the rectangle against the polygon, I check the polygon against the
# rectangle? I check each segment of the polygon border to see if it passes through the interior
# of the rectangle, and if it does, reject the rectangle. I can also test a point in the middle of
# the rectangle to see if it's inside the polygon. (Maybe try that first, for speed.)

# Since the lines are only either vertical or horizontal, we can get away with a simple algorithm
def lines_cross(l1v1: Vector, l1v2: Vector, l2v1: Vector, l2v2: Vector) -> bool:
	dv1 = l1v2 - l1v1
	dv2 = l2v2 - l2v1
	if dv1.dot(dv2) != 0:
		# The lines are parallel and (for our purposes) do not intersect
		return False
	elif abs(dv1.x) > 0:
		# Line 1 is horizontal; line 2 is vertical
		if (l2v1.x > min(l1v1.x, l1v2.x) and l2v1.x < max(l1v1.x, l1v2.x)) and \
		   (l1v1.y > min(l2v1.y, l2v2.y) and l1v1.y < max(l2v1.y, l2v2.y)):
			return True
	else:
		# Line 1 is vertical; line 2 is horizontal
		if (l1v1.x > min(l2v1.x, l2v2.x) and l1v1.x < max(l2v1.x, l2v2.x)) and \
		   (l2v1.y > min(l1v1.y, l1v2.y) and l2v1.y < max(l1v1.y, l1v2.y)):
			return True
	return False

# Crud, that didn't work, even in the example. It's the corners -- the polygon border never actually
# crosses the edges of the size-50 rectangle from part 1; there's just a corner missing. The fact
# that part of the rectangle is going to be collinear with the polygon boundary makes this
# obnoxious. Someone online suggests checking for the presence of polygon corners in the rectangle,
# which seems reasonable. Unfortunately, even checking for whether a tile is in the polygon is
# awkward because of the damned corners. I don't feel like dealing with this anymore, so I'm giving
# up and using someone else's code to get the answer. We'll call this one a failure.

# The answer for my input was: 1539809693

	
"""
# Try each rectangle in descending order of size and check for intersections with the polygon
for rect in rect_sizes:
	c1 = rect[0]
	c3 = rect[1]
	c2 = Vector(c1.x, c3.y)
	c4 = Vector(c3.x, c1.y)
	
	intersection = False
	for t in range(len(red_tiles)):
		t1 = red_tiles[t]
		t2 = red_tiles[(t + 1) % len(red_tiles)]
		if lines_cross(c1, c2, t1, t2):
			intersection = True
			break
		if lines_cross(c2, c3, t1, t2):
			intersection = True
			break
		if lines_cross(c3, c4, t1, t2):
			intersection = True
			break
		if lines_cross(c4, c1, t1, t2):
			intersection = True
			break
		if t1.x > min(c1.x, c3.x) and t1.x < max(c1.x, c3.x) and t1.y > min(c1.y, c3.y) and t1.y < max(c1.y, c3.y):
			intersection = True
			break
	
	if not intersection:
		print(f"Part 2: The largest possible rectangle area is: {rect[2]} {rect[0]} {rect[1]}")
		break
"""
