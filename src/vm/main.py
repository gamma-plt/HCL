import os
import sys
import info
import lang
import debugger

MEMORY_SIZE = 34
WORD_SIZE = 16

mem = ['0' * WORD_SIZE for i in range(MEMORY_SIZE)]
amv = {'summation' : ('BOOL', '0x20')}
args = []
world = ['add', 'ret', 'r1', 'r2', 'r3', 'r4', 'r5']

def execute(instruction):
	index, instruction = instruction
	inst_args = instruction.split(' ')

	print inst_args

	if len(inst_args) == 1:
		pass	
	elif len(inst_args) == 2:
		pass
	elif len(inst_args) == 3:
		pass
	else:
		pass


def execute_instructions(instructions):
	for instruction in instructions:
		execute(instruction)

def remove_comments(parsed_file):
	ans = []

	for idx, itm in parsed_file:
		element = itm

		if lang.COMMENT_SEPARATOR in itm:
			index = itm.index(lang.COMMENT_SEPARATOR)
			element = itm[:index]

		ans.append((idx, element.strip(' ').strip('\n')))

	return ans

def get_blocks(fileobject):
	lines = [(i, line) for i, line in enumerate(fileobject) if line != '\n']
	lines = remove_comments(lines)	
	blocks = [(i, line) for i, line in lines if line[0] != '\t']

	lower_bounds = [index for index, line in blocks]
	upper_bounds = lower_bounds[1:] + [lower_bounds[-1]]

	parsed_blocks = []

	i = 0
	while lower_bounds[i] != upper_bounds[i]:
		a, b = lower_bounds[i], upper_bounds[i]
		parsed_blocks.append(filter(lambda x : x[0] in range(a, b), lines))
		i += 1

	a, b = lower_bounds[i], upper_bounds[i]
	parsed_blocks.append(filter(lambda x : x[0] in range(a, b + 1), lines))

	for instructions in parsed_blocks:
		execute_instructions(instructions)

def process_file(filename):
	fileobject = open(filename, 'r')
	blocks = get_blocks(fileobject)

def main():

	arguments = sys.argv
	if len(arguments) != 2:
		info.print_usage()
	else:
		filename = sys.argv[-1]
		if not os.path.isfile(filename):
			info.print_file_not_found(filename)
		else:
			process_file(filename)
			
	'''
	dbg = debugger.Debugger(mem, amv, args, world, MEMORY_SIZE)
	dbg.execute('pamv')
	'''


if __name__ == '__main__':
	main()
