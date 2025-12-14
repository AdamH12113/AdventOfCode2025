import re, sys, copy

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

# Process the input. It's a list of number ranges (fresh ingredient IDs) follow by a list of numbers
# (available ingredient IDs).
ranges_text, available_text = input_text.split('\n\n')
ranges = set((int(r[0]), int(r[1])) for r in [rt.split('-') for rt in ranges_text.split('\n')])
available = [int(n) for n in available_text.split('\n')]

# Part 1: How many available ingredient IDs are fresh? Fresh IDs are those found in one of the listed
# ranges. Python range objects work well for this since they can check for membership in constant time.
fresh_ids = sum(any(id in range(r[0], r[1]+1) for r in ranges) for id in available)
print(f"Part 1: The number of fresh IDs is: {fresh_ids}")

# Part 2: How many possible ingredient IDs are fresh? The given ranges overlap, so we have to take
# that into account.
def ranges_overlap(r1: tuple, r2: tuple) -> bool:
	return not (r1[1] < r2[0] or r2[1] < r1[0])

# This assumes the ranges overlap
def merge_ranges(r1: tuple, r2: tuple) -> tuple:
	return (min(r1[0], r2[0]), max(r1[1], r2[1]))

# We just want to keep iterating until we stop finding merge candidates. The loop conditions are the
# only complicated part.
merge_done = True
while merge_done:
	range_buf = set()
	merge_done = False
	while len(ranges) > 0:
		r1 = ranges.pop()
		for r2 in copy.deepcopy(ranges):
			if ranges_overlap(r1, r2):
				r1 = merge_ranges(r1, r2)
				ranges.remove(r2)
				merge_done = True
		range_buf.add(r1)
	ranges = range_buf

num_fresh_ids = sum((r[1] - r[0] + 1) for r in ranges)
print(f"Part 2: The number of possible fresh IDs is: {num_fresh_ids}")
