import re, sys, copy
from functools import reduce
from operator import mul, add

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

# Part 2: The numbers themselves are now in columns! What is the grand total now? Alignment now
# matters since a single digit in a row can be in either the leftmost or rightmost column of a
# problem. The operator is always in the leftmost column. We have to fully reprocess the input.
new_op = True
grand_total = 0
numbers = []
for col in range(len(rows_text[0])-1, 0-1, -1):
	if new_op:
		numbers = []
		op = None
		new_op = False
	num = 0
	for row in range(len(rows_text)):
		char = rows_text[row][col]
		if char == '+':
			op = add
		elif char == '*':
			op = mul
		elif rows_text[row][col] != ' ':
			num = 10*num + int(rows_text[row][col])
	if num == 0:
		continue
	numbers.append(num)
	if op is not None:
		answer = reduce(op, numbers, 1 if op is mul else 0)
		grand_total += answer
		new_op = True
print(f"Part 2: The grand total is: {grand_total}")





