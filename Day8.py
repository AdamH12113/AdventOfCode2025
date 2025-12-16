import re, sys, copy, networkx
from Vector import Vector3

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

# Process the input. It's a list of comma-separated X/Y/Z coordinates of junction boxes. I'm abusing
# Python assignment expressions a bit here.
boxes = [Vector3(int(c[0]), int(c[1]), int(c[2])) for line in input_text.split('\n') if (c := line.split(','))]

# Connect together the thousand closest pairs of boxes. Connected boxes form a circuit. What is the
# product of the sizes of the three largest circuits? This is a graph puzzle, and I have learned the
# hard way in previous years that the second half will probably need some kind of graph algorithm
# that I really don't want to implement myself, so let's do the smart thing and start off by using
# a graph library. But first, we need to find the distances between each pair of nodes.
num_connections = 10 if '--example' in sys.argv else 1000

distances = []
for b1 in range(len(boxes)):
	for b2 in range(b1+1, len(boxes)):
		distances.append((boxes[b1], boxes[b2], abs(boxes[b1] - boxes[b2])))
distances.sort(key = lambda dist_tuple: dist_tuple[2])

# In graph theory, a group of connected nodes is called a "component". NetworkX can easily give us
# the sizes of every component in the graph, and in fact there's an example for that in their docs:
# https://networkx.org/documentation/networkx-3.2.1/reference/algorithms/generated/networkx.algorithms.components.connected_components.html#networkx.algorithms.components.connected_components
G = networkx.Graph()
for d in range(num_connections):
	dt = distances[d]
	G.add_edge(dt[0], dt[1])
component_sizes = [len(c) for c in sorted(networkx.connected_components(G), key=len, reverse=True)]
product = component_sizes[0] * component_sizes[1] * component_sizes[2]
print(f"Part 1: The product of the three largest circuit sizes is: {product}")

# Part 2: Continue connecting the closest unconnected pairs of junction boxes together until all of
# the boxes are in a single circuit. What is the product of the X coordinates of the last two
# junction boxes connected? This is a straightforward extension of part 1, although it takes a while
# to execute.
G = networkx.Graph()
G.add_nodes_from(boxes)
for d in range(len(distances)):
	dt = distances[d]
	G.add_edge(dt[0], dt[1])
	if networkx.is_connected(G):
		print(dt[0], dt[1])
		product = dt[0].x * dt[1].x
		print(f"Part 2: The product of the X coordinates of the last two boxes is: {product}")
		break

	
