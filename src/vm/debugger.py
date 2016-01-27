import globalenv

from tabulate import tabulate

class Debugger(object):
	'''The class Debugger, implements the logic of a very simple VM hardware
	debugger. The purpose of an object of this class, is to assistes the development,
	testing and debugging process of the VM hardware, specified and implemented
	in the file hardware.py. The usage is described in the self.run() method, the
	unique that must be used by client code. Use it whith precuation, you can get
	Python error messages if not used properly

	Attributes:
		vm : A HCLVirtualMachine object, the definition is included in the
		hardware.py file 

		mem_size : The length of the words of the VM memory
	'''

	# The commands of the debugger
	COMMANDS = ['pmem', 'pamv', 'pstk', 'prgs']

	# Commands for vm manipulation
	COMMANDS += ['set', 'mov', 'not', 'and', 'or', 'inc']
	COMMANDS += ['dec', 'add', 'sub', 'div', 'mod']
	COMMANDS += ['print', 'push', 'call', 'halt']

	QUITTER = 'quit'

	# Wrong command message
	ERROR_INDICATOR = 'WRONG COMMAND'
	SYNTAX_ERROR = 'MALFORMED COMMAND'

	# The debugger propmt
	INPUT_PROMPT = '(cmd) '

	def __init__(self, vm, mem_size):
		'''Initilizes a debugger object, the vm, has to have as fields,
		a main memory, an associations of variables with values, a stack
		of arguments, an association of registers and values. The mem_size
		is for hexadecimal representation of each address.'''

		self.vm = vm
		self.mem = vm.memory
		self.amv = vm.amv
		self.args = vm.args
		self.regs = vm.regs
		self.memory_size = mem_size
		self.length = len(str(hex(mem_size)))

	# Ouput handling methods

	def _print_memory(self):
		'''Prints the content of each address of the VM's memory, if prints
		an asociation between the address as hexadecimal, and the location
		value as binary string'''

		for i, itm in enumerate(self.mem):
			print str(hex(i)).zfill(self.length), ' : ', itm

	def _print_amv(self):
		'''Prints the content of each variable defined in the VM, its type,
		its address and its value in binary, without the occupation bit
		flag, that is, just the original binary string.
		'''

		table = []

		for itm in self.amv:

			packed = self.amv[itm]
			vm_type, vm_add = packed
			index = int(vm_add, 0)
			vm_val = self.mem[index][1:]

			table.append([itm, vm_type, str(vm_add).zfill(self.length), vm_val])

		print tabulate(table)

	def _print_args(self):
		'''Prints the current value of the stack items, it could be empty
		or filled with some values.
		'''

		table = []

		i = len(self.args.items) - 1
		while i >= 0:
			itm = self.args.items[i]
			table.append([itm.zfill(globalenv.WORD_SIZE + 1)])
			i -= 1

		print tabulate(table)

	def _print_regs(self):
		'''Prints the address of each register in the VM hardware, the address
		is the position in memeory that has the value pointed by the register
		'''

		table = []

		for name in self.regs:
			table.append([name.upper(), self.regs[name].zfill(self.length)])

		print tabulate(table)

	# Instructions for enviroment change

	def _set(self, name, name_type):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of variable allocation'''
		self.vm._set(name, name_type)

	def _mov(self, variable, value):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of moving some value of the value of some variable
		to another variable'''
		self.vm._mov(variable, value)

	def _not(self, variable):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of negate a whole binary string, which is the value
		of the given variable'''
		pass

	def _and(self, variable):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of get the logical and of a whole binary string, 
		which is the value of the given variable'''
		pass

	def _or(self, variable):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of get the logical or of a whole binary string, 
		which is the value of the given variable'''
		pass

	def _inc(sefl, variable):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of incrementing in one the value of some binary_string,
		which is the value of the given variable passed as argument'''
		pass

	def _dec(sefl, variable):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of decrementing in one the value of some binary_string,
		which is the value of the given variable passed as argument'''
		pass

	def _add(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of adding the the value of the variable and the 
		operator's value'''
		pass

	def _sub(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of substract the the value of the variable and the 
		operator's value'''
		pass

	def _mul(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of multiply the the value of the variable and the 
		operator's value'''
		pass

	def _div(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of divide the the value of the variable and the 
		operator's value'''
		pass

	def _mod(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose to get the module of the the value of the variable 
		and the operator's value'''
		pass

	def _print(self, variable):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of printing the current value of some variable 
		allocated in the vm's memory'''
		pass

	def _halt(self):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose to quit the execution of the program by the virtual 
		machine'''
		pass

	def _push(self, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of pushin some value or a variable's value to the
		vm arguments stack'''
		pass

	def _call(self, function):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of calling a function, as defined in atomic library
		'''
		pass

	def _free(self, function):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of deallocating a variable'''
		pass

	# User interface

	def _execute_simple_command(self, command):
		'''Specifies the logic for each self.COMMAND variable, it the commands
		has just an instruction and no operators'''

		# Print memory
		if command == self.COMMANDS[0]:
			self._print_memory()

		# Print amv
		elif command == self.COMMANDS[1]:
			self._print_amv()

		# Print stack
		elif command == self.COMMANDS[2]:
			self._print_args()

		# Print registers
		elif command == self.COMMANDS[3]:
			self._print_regs()

		# Print wrong command
		else:
			print self.ERROR_INDICATOR

	def _execute_compound_command(self, command, arguments):
		'''Specifies the logic for each compound (with arguments or operators) self.COMMAND 
		variable'''

		# Set a variable
		if command == self.COMMANDS[4]:

			association = {'integer' : 'INTEGER', 'boolean' : 'BOOLEAN', \
										'char' : 'CHAR'}

			name = arguments[0].lower()
			name_type = arguments[1].lower()

			if name_type in association:
				self._set(name, association[name_type])
			else:
				if '#' in name_type:
					parse = name_type.split('#')
					if parse[0] in association:
						self._set(name, name_type)
					else:
						print self.SYNTAX_ERROR
				else:
					print self.SYNTAX_ERROR

		# Move a varible or value to an specific cell pointed by a variable
		elif command == self.COMMANDS[5]:
			name = arguments[0].lower()
			operator = arguments[1].lower()

			self._mov(name, operator)

		# Negate in place a whole variable's value
		elif command == self.COMMANDS[6]:
			pass

		# Get in place the logical and of some variable's value
		elif command == self.COMMANDS[7]:
			pass

		# Get in place the logical or of some variable's value
		elif command == self.COMMANDS[8]:
			pass

		# Increment in place the logical value of some variable's value
		elif command == self.COMMANDS[9]:
			pass

		# Decrease in place the logical value of some variable's value
		elif command == self.COMMANDS[10]:
			pass

		# Add in place a variable's value and a value or another variable's value
		# given as parameter
		elif command == self.COMMANDS[11]:
			pass

		# Substract in place a variable's value and a value or another variable's value
		# given as parameter
		elif command == self.COMMANDS[12]:
			pass

		# Divide in place a variable's value and a value or another variable's value
		# given as parameter
		elif command == self.COMMANDS[13]:
			pass

		# Get in place the module of a variable's value and a value or another variable's value
		# given as parameter
		elif command == self.COMMANDS[14]:
			pass

		# Print a variable's value 
		elif command == self.COMMANDS[15]:
			pass

		# Push a variable to the stack
		elif command == self.COMMANDS[16]:
			pass

		# Call a function
		elif command == self.COMMANDS[17]:
			pass		

		# Print wrong command
		else:
			print self.ERROR_INDICATOR

	def run(self):
		'''Receive the command and executes it as properly defined by
		self._execute. It should be called by the client code'''

		command = raw_input(self.INPUT_PROMPT)
		command = command.lower()
		parse = command.split()		

		while command != self.QUITTER:
			command = parse[0]

			if len(parse) == 1:

				if command == self.COMMANDS[18]:
					while True:
						pass

				self._execute_simple_command(command)

			else:
				args = parse[1:]
				self._execute_compound_command(command, args)

			command = raw_input(self.INPUT_PROMPT)
			command = command.lower()
			parse = command.split()