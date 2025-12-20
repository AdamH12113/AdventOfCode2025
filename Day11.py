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

# Process the input. Each line contains a three-letter device name followed by a list of three-
# letter outputs.
Node = namedtuple('Node', ['inputs', 'outputs'])
nodes = {}
for line in input_text.split('\n'):
	source = line[:3]
	if source not in nodes:
		nodes[source] = Node([], [])
	dests = line[5:].split(' ')
	for dest in dests:
		if dest not in nodes:
			nodes[dest] = Node([], [])
		nodes[source].outputs.append(dest)
		nodes[dest].inputs.append(source)

# Special handling because there are two example inputs
nodes2 = {}
if '--example' in sys.argv:
	with open('Example11b.txt', 'rt') as f:
		input_text2 = f.read()[:-1]
	for line in input_text2.split('\n'):
		source = line[:3]
		if source not in nodes2:
			nodes2[source] = Node([], [])
		dests = line[5:].split(' ')
		for dest in dests:
			if dest not in nodes2:
				nodes2[dest] = Node([], [])
			nodes2[source].outputs.append(dest)
			nodes2[dest].inputs.append(source)


# Part 1: How many possible paths are there between the "you" node and the "out" node? A backwards
# depth-first search will do the job, but let's add memorization for performance reasons.
num_paths_cache = {}
def find_num_paths(nodes: dict, src: str, dest: str) -> int:
	node = nodes[dest]
	if (src, dest) in num_paths_cache:
		return num_paths_cache[(src, dest)]
	elif len(node.inputs) == 0:
		return 0
	elif src in node.inputs:
		return 1
	
	paths = 0
	for input in node.inputs:
		paths += find_num_paths(nodes, src, input)
	num_paths_cache[(src, dest)] = paths
	return paths

num_paths = find_num_paths(nodes, 'you', 'out')
print(f"Part 1: The number of possible paths is: {num_paths}")

# Part 2: How many possible paths are there between "svr" and "out" that also visit "dac" and "fft"
# in either order? I think there are only two possible ways of doing this, so we can just add them:
#   svr -> dac -> fft -> out
#   svr -> fft -> dac -> out
if '--example' in sys.argv:
	nodes = nodes2

svr_dac_paths = find_num_paths(nodes, 'svr', 'dac')
svr_fft_paths = find_num_paths(nodes, 'svr', 'fft')
dac_fft_paths = find_num_paths(nodes, 'dac', 'fft')
fft_dac_paths = find_num_paths(nodes, 'fft', 'dac')
dac_out_paths = find_num_paths(nodes, 'dac', 'out')
fft_out_paths = find_num_paths(nodes, 'fft', 'out')

svr_dac_fft_out_paths = svr_dac_paths * dac_fft_paths * fft_out_paths
svr_fft_dac_out_paths = svr_fft_paths * fft_dac_paths * dac_out_paths
num_paths = svr_dac_fft_out_paths + svr_fft_dac_out_paths
print(f"Part 2: The number of possible paths is: {num_paths}")
