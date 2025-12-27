import re, sys, copy, networkx

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

# Process the input. Each line has three parts: A list of indicator lights with desired states for
# each, a list of buttons and which indicator lights they invert, and a list of joltage requirements
# for the lights.
class Machine:
	lights: list[bool]
	desired_lights = list[bool]
	num_lights: int
	buttons: list[tuple[int]]
	num_buttons: int
	desired_joltages: list[int]
	
	def __init__(self, line: str):
		light_str = line[1:line.index(']')]
		self.num_lights = len(light_str)
		self.lights = 0x0
		self.desired_lights = 0x0
		for b in range(len(light_str)):
			if light_str[b] == '#':
				self.desired_lights += 2**b
		
		button_str = line[line.index(']')+2:line.index('{')-1]
		self.buttons = []
		for button in button_str.split(' '):
			self.buttons.append(sum(2**int(b) for b in re.findall(r'\d+', button)))
		self.num_buttons = len(self.buttons)
		
		self.desired_joltages = [int(n) for n in line[line.index('{')+1:-1].split(',')]
		self.joltages = [0] * len(self.desired_joltages)
	
	def __repr__(self) -> str:
		return f'[{self.desired_lights}] [{self.lights}] ({self.buttons}) {{{self.joltages}}}'
	
#	def reset(self):
#		self.lights = 0x0
#		self.joltages = [0] * len(self.desired_joltages)
	
#	def push_button(self, b: int):
#		self.lights ^= self.buttons[b]
	
	def push_buttons(self, bs: int):
		self.lights = 0x0
		button = 0
		while bs != 0:
			if bs & 0x1 == 0x1:
				self.lights ^= self.buttons[button]
			button += 1
			bs >>= 1
	
	def lights_valid(self) -> bool:
		return self.lights == self.desired_lights

machines = [Machine(line) for line in input_text.split('\n')]

# Part 1: What is the fewest button presses required to correctly configure the indicator lights on
# all of the machines? Pressing a button twice does nothing, so combinations of single button
# presses are the full space of possibilities. I'm going to start with a brute-force method trying
# each combination of presses in order by number of presses. To generate the combinations, I'm using
# an algorithm taken from here: https://www.alexbowe.com/popcount-permutations/
def next_popcount_permutation(n: int):
	t = (n | (n - 1)) + 1
	w = t | ((((t & -t) // (n & -n)) >> 1) - 1)
	return w

def find_fewest_presses(m: Machine) -> int:
	for num_presses in range(1, m.num_buttons + 1):
		buttons = 2**num_presses - 1
		while buttons < 2**m.num_buttons:
			m.push_buttons(buttons)
			if m.lights_valid():
				return num_presses
			buttons = next_popcount_permutation(buttons)
	print('fail')

total_presses = 0
for machine in machines:
	presses = find_fewest_presses(machine)
	total_presses += presses
print(f"Part 1: The total number of button presses is: {total_presses}")

# Part 2: The buttons now boost joltages instead of toggling lights. Multiple button presses are now
# valid, which means this part isn't amenable to brute force. (No surprise there.) I feel like a
# linear algebra approach should be possible here, but if there are multiple solutions I'm not sure
# how that would work.

# After a fair bit of searching, I've found that what we have is called a "system of linear
# Diophantine equations", and solving one is nontrivial. Even the hardcore folks in the Reddit
# forum are all talking about the difficulty of this problem. I don't mind branching out and
# learning a new algorithm or even a bit of a new subject, but when people are talking about how
# theorem provers are the best solution, I don't think that the puzzle is within the normal scope
# of the Advent of Code. I'm going to run someone else's code to get the solution.

# My answer is 20172. I had to try a *second* person's code because the first person's gave the
# wrong answer (20182), which I think proves my point about the puzzle. Nonetheless, we can consider
# this a failure on my part.
