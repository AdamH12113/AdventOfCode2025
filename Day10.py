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
	joltages: list[int]
	
	def __init__(self, line: str):
		light_str = line[1:line.index(']')]
		self.num_lights = len(light_str)
		self.lights = [False] * self.num_lights
		self.desired_lights = [(c == '#') for c in light_str]
		
		button_str = line[line.index(']')+2:line.index('{')-1]
		self.buttons = [eval(s) for s in button_str.split(' ')]
		
		self.joltages = [int(n) for n in line[line.index('{')+1:-1].split(',')]

machines = [Machine(line) for line in input_text.split('\n')]

	



