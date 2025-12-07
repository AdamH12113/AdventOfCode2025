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

# Process the input. Each line ("battery bank") is a sequence of digits ("batteries").
banks = [[int(b) for b in bank] for bank in input_text.split('\n')]

# Part 1: Choose two batteries per bank. The joltage from the bank is given by the battery digits,
# in order. What is the sum of the maximum joltages attainable for each bank? A larger first digit
# will always give a higher joltage, so this part is pretty simple. The main edge case is if the
# largest digit in the list comes last, since a two-digit number will always be larger.
joltage_sum = 0
for bank in banks:
	first_digit = max(bank[:-1])
	second_digit = max(bank[bank.index(first_digit) + 1:])
	joltage_sum += first_digit*10 + second_digit
print(f"Part 1: The total output joltage is: {joltage_sum}")

# Part 2: Now we choose twelve batteries per bank. We can solve this similar to the way we dealt
# with the edge case in the first part.
joltage_sum = 0
for bank in banks:
	joltage = 0
	min_index = 0
	max_index = -11
	for digit in range(12):
		batt = max(bank[min_index:max_index or None])  # None means include the end of the list
		joltage = 10*joltage + batt
		min_index = bank.index(batt, min_index) + 1
		max_index += 1
	joltage_sum += joltage
print(f"Part 2: The total output joltage is: {joltage_sum}")


