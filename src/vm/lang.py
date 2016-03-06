COMMENT_SEPARATOR = ';;'
HALT_INSTRUCTION = 'halt'

cmp_blocks = ['equ', 'neq', 'slt', 'sgt', 'leq', 'geq']
blocks = ['do', 'if', 'clc', 'act'] + cmp_blocks
instructions = ['set', 'mov', 'and', 'not', 'xor', 'or', 'add', 
					'sub', 'dec', 'inc', 'mul', 'div', 'mod', 'print', 'push', 'call',
					'free', 'cmp', 'readint', 'readchr']

binary_intructions = ['set', 'mov', 'and', 'or', 'add', 'sub', 'mul', 'div', 'mod', 'cmp', 'xor']
unary_instructions = ['not', 'dec', 'inc', 'push', 'call', 'free', 'readint', 'readchr']
single_composed_instructions = ['halt', 'skip']
single_instructions = single_composed_instructions + ['gss', 'print']

def report_syntax_error(line):
	print 'SYNTAX ERROR AT LINE: ' + str(line + 1)
	quit()

class Node(object):
    def __init__(self, line, level, command, args):
    	self.level = level
    	self.line = line
        self.command = command
        self.args = args
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __str__(self):
    	ans = str(self.level) + ' '
    	ans += self.command + ' : ' + ' - '.join(self.args) + '\n'

    	for child in self.children:
    		ans += str(child)

    	return ans

def shape_node(line, instruction, level):
	if instruction != '':
		parsed_instruction = instruction.split()
		command = ''
		if instruction.strip()[0] == '[':
			command = 'gss'
		elif parsed_instruction[0] == 'halt':
			command = 'halt'
		elif parsed_instruction[0] == 'skip':
			command = 'skip'
		elif parsed_instruction[0] in ['equ:', 'neq:', 'slt:', 'sgt:', 'leq:', 'geq:']:
			command = parsed_instruction[0][:-1]
		else:
			command = instruction[:-1] if len(parsed_instruction) == 1 else parsed_instruction[0]

		arguments = []

		if len(parsed_instruction) > 1:
			i = 1
			while i != len(parsed_instruction):
				arguments.append(parsed_instruction[i])
				i += 1
			
		node = Node(line, level, command.strip(), arguments)
		return node

def get_node_level(instruction):
	level = 1
	i = 0
	while instruction[i] == '\t':
		level += 1
		i += 1
	return level

def get_syntax_tree(nested_blocks):
	root = Node(-1, 0, 'root', [])
	references = {0 : root}
	current = 0

	for line, instruction in nested_blocks:

		if instruction != '':

			level = get_node_level(instruction)
			node = shape_node(line, instruction, level)
			references[level - 1].add_child(node)
			references[level] = node

	return references[0]

def check_binary_instruction(node):

	line = node.line
	command = node.command
	args = node.args
	children = node.children

	if len(args) != 2 or len(children) != 0:
		report_syntax_error(line)

def check_unary_instruction(node):
	
	line = node.line
	command = node.command
	args = node.args
	children = node.children

	if len(args) != 1 or len(children) != 0:
		report_syntax_error(line)

def check_single_instruction(node, composed=True):
	
	line = node.line
	command = node.command
	args = node.args
	children = node.children

	if composed:
		# halt, skip
		if len(args) != 0 or len(children) != 0:
			report_syntax_error(line)

	else:
		# gss, print
		if len(args) == 0 or len(children) != 0:
			report_syntax_error(line)


def check_do_node(node):

	gss_commands = filter(lambda node : node.command == 'gss', node.children)

	if len(gss_commands) == 0:
		print 'MISSED GSS BLOCK IN DO BLOCK: ' + str(node.line)
		report_syntax_error(node.line)

	elif len(gss_commands) != 1:
		print 'TWO GUARDED VARIABLES DECLARATION'
		report_syntax_error(gss_commands.pop(-1).line)
	
	else:
		gss_command = gss_commands.pop()
		gss_args = gss_command.args

	clc_commands = filter(lambda node : node.command == 'clc', node.children)

	if len(clc_commands) == 0:
		print 'MISSED CLC BLOCK IN DO BLOCK: ' + str(node.line)
		report_syntax_error(node.line)

	elif len(clc_commands) != 1:
		print 'TWO GUARDED CALCULATION BLOCKS DECLARED'
		report_syntax_error(clc_commands.pop(-1).line)
			
	act_commands = filter(lambda node : node.command == 'clc', node.children)

	if len(act_commands) == 0:
		print 'MISSED ACT BLOCK IN DO BLOCK: ' + str(node.line)
		report_syntax_error(node.line)

	for child in node.children:
		if child.command not in ['gss', 'clc', 'act']:
			report_syntax_error(child.line)

	else:
		return True

def check_if_node(node):

	gss_commands = filter(lambda node : node.command == 'gss', node.children)

	if len(gss_commands) == 0:
		print 'MISSED GSS BLOCK IN DO BLOCK: ' + str(node.line)
		report_syntax_error(node.line)

	elif len(gss_commands) != 1:
		print 'TWO GUARDED VARIABLES DECLARATION'
		report_syntax_error(gss_commands.pop(-1).line)

	for child in node.children:
		if child.command == 'clc':
			report_syntax_error(child.line)

	else:
		return True

def check_actclcnode(node, allowed_instructions):
	flag = True
	error_line = ''

	for child in node.children:
		if child.command not in allowed_instructions:
			flag = False
			error_line = child.line
			break

	return error_line, flag

def check_syntax_tree(syntax_treenode):

	level = syntax_treenode.level
	line = syntax_treenode.line
	command = syntax_treenode.command
	args = syntax_treenode.args
	children = syntax_treenode.children

	if command in binary_intructions:
		check_binary_instruction(syntax_treenode)

	elif command in unary_instructions:
		check_unary_instruction(syntax_treenode)

	elif command in single_instructions:
		if command in single_composed_instructions:
			check_single_instruction(syntax_treenode, True)
		else:
			check_single_instruction(syntax_treenode, False)

	elif command in ['if', 'do']:
		if len(args) != 0 or len(children) == 0:
			report_syntax_error(line)

		checker = check_if_node if command == 'if' else check_do_node

		if checker(syntax_treenode):
			for child in children:
				check_syntax_tree(child)	

	elif command in ['act', 'clc']:

		flag = 1 if command == 'act' else 0
		act_list = blocks + instructions + ['skip']
		clc_list = cmp_blocks + instructions
		allowed_instructions = act_list if command == 'act' else clc_list

		if len(args) != flag or len(children) == 0:
			report_syntax_error(line)

		error_line, flag = check_actclcnode(syntax_treenode, allowed_instructions)

		if not flag:
			report_syntax_error(error_line)

		for child in children:
			check_syntax_tree(child)	

	elif command in cmp_blocks:
		if len(args) != 0 or len(children) == 0:
			report_syntax_error(line)

		for child in children:
			check_syntax_tree(child)
			
	else:
		report_syntax_error(line)