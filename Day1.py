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

# Process the input. Each line is a rotation consisting of a direction ('L' or 'R') and the number
# of positions to rotate. We can interpret the left direction as negative and the right as positive.
input_lines = input_text.split('\n')
rotations = [(-int(line[1:]) if line[0] == 'L' else int(line[1:])) for line in input_lines]

# Part 1: Find the number of times the dial is left pointing at zero after any rotation.
dial = 50
zero_count = 0
for rotation in rotations:
	dial = (dial + rotation) % 100
	if dial == 0:
		zero_count += 1
print(f"Part 1: The password is: {zero_count}")

# Part 2: Find the number of times the dial is left pointing at zero at any time during any
# rotation. The input isn't very long but let's do this efficiently anyway using division. Python's
# modulus division is a bit unusual so we have to spell out what we want.
dial = 50
zero_count = 0
for rotation in rotations:
	full_rotations = int(rotation / 100)
	partial_rotation = rotation - full_rotations*100
	zero_count += abs(full_rotations)
	if dial != 0 and (dial + partial_rotation >= 100 or dial + partial_rotation <= 0):
		zero_count += 1
	dial = (dial + partial_rotation) % 100
print(f"Part 1: The password is: {zero_count}")
