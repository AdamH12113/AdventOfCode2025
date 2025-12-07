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

# Process the input. It's one long line consisting of a comma-separated list of number ranges. The
# numbers in the range are separated by hyphens.
ranges_text = [range_text.split('-') for range_text in input_text.split(',')]
ranges = [(int(a), int(b)) for a,b in ranges_text]

# Part 1: Find the sum of the invalid IDs. Invalid IDs are numbers that consist of a sequence of
# digits repeated twice.
invalid_id_sum = 0
for r in ranges:
	for id in range(r[0], r[1]+1):
		sid = str(id)
		if sid[:len(sid)//2] == sid[len(sid)//2:]:
			invalid_id_sum += id
print(f"Part 1: The sum of the invalid IDs is: {invalid_id_sum}")

# Part 2: Invalid IDs can now consist of a sequence of digits repeated *at least* twice. What is the
# sum of the invalid IDs now? We can do this by finding all the factors of the ID length and checking
# the ones that divide the length evenly.
invalid_id_sum = 0
for r in ranges:
	for id in range(r[0], r[1]+1):
		sid = str(id)
		size = len(sid)
		for div in range(2, len(sid)+1):
			if div*(size // div) == size:
				mismatch = False
				section_size = size // div
				for section in range(div - 1):
					if sid[section*section_size:(section+1)*section_size] != sid[(section+1)*section_size:(section+2)*section_size]:
						mismatch = True
				if not mismatch:
					invalid_id_sum += id
					break
print(f"Part 2: The sum of the invalid IDs is: {invalid_id_sum}")
