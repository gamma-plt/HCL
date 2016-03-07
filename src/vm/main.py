# RUN AS: python main.py ../../examples/vm/example1.vhcl

import os
import sys
import info
import lang
import hardware
import debugger
import globalenv

MEMORY_SIZE = globalenv.MEMORY_SIZE
DEBUGGING = info.DEBUGGING

def remove_comments(parsed_file):
	ans = []

	for idx, itm in parsed_file:
		element = itm

		if lang.COMMENT_SEPARATOR in itm:
			index = itm.index(lang.COMMENT_SEPARATOR)
			element = itm[:index]
			element = element.lower()

		ans.append((idx, element.strip(' ').strip('\n')))

	return ans

def get_blocks(fileobject):
	lines = [(i, line) for i, line in enumerate(fileobject) if line != '\n']
	lines = remove_comments(lines)	
	blocks = [(i, line) for i, line in lines if line and line[0] != '\t']

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

	return parsed_blocks

def process_file(filename):
	fileobject = open(filename, 'r')
	blocks = get_blocks(fileobject)

	_, halt_ist = blocks[-1][0]
	if halt_ist != lang.HALT_INSTRUCTION:
		lang.report_syntax_error(_)

	whole_program = []

	for block in blocks:
		for blck in block:
			whole_program.append(blck)

	syntax_tree = lang.get_syntax_tree(whole_program)
	
	for node in syntax_tree.children:
		lang.check_syntax_tree(node)

	return syntax_tree.children

def main():
	arguments = sys.argv
	if len(arguments) != 2:
		info.print_usage()
	else:
		filename = sys.argv[-1]
		if not os.path.isfile(filename):
			info.print_file_not_found(filename)
		else:
			vm = hardware.HCLVirtualMachine()
			syntax_tree = process_file(filename)
			vm.process_syntax_tree(syntax_tree)

			if DEBUGGING:

				db = debugger.Debugger(vm, MEMORY_SIZE)
				db.run()

if __name__ == '__main__':
	main()