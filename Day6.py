import re, sys, copy
from functools import reduce
from operator import mul

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

# Process the input. It's a list of math problems arranged in columns. Each column contains a list
# of numbers and an operation at the bottom.
rows_text = input_text.split('\n')
rows = [[int(n) for n in line.split()] for line in rows_text[:-1]]
ops = rows_text[-1].split()
num_problems = len(ops)

# Part 1: Find the sum of the answers to each problem (the "grand total").
grand_total = 0
for p in range(num_problems):
	if ops[p] == '+':
		answer = sum(row[p] for row in rows)
	else:
		answer = reduce(mul, (row[p] for row in rows), 1)
	grand_total += answer
print(f"Part 1: The grand total is: {grand_total}")

# Part 2: The numbers themselves are now in columns! What is the grand total now?
grand_total = 0


