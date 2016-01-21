from tabulate import tabulate

class Debugger(object):
	'''The class Debugger, implements the logic of a very simple VM hardware
	debugge. The purpose of an object of this class, is to assistes the development,
	testing and debugging process of the VM hardware, specified and implemented
	in the file hardware.py. The usage is described in the self.run() method, the
	unique that must be used by client code.

	Attributes:
		vm : A HCLVirtualMachine object, the definition is included in the
		hardware.py file 

		mem_size : The length of the words of the VM memory
	'''

	COMMANDS = ['pmem', 'pamv', 'pstk', 'prgs', 'quit']
	ERROR_INDICATOR = 'WRONG COMMAND'
	INPUT_PROMPT = '(cmd) '

	def __init__(self, vm, mem_size):
		'''Initilizes a debugger object, the vm, has to have as fields,
		a main memory, an associations of variables with values, a stack
		of arguments, an association of registers and values. The mem_size
		is for hexadecimal representation of each address.'''

		self.mem = vm.memory
		self.amv = vm.amv
		self.args = vm.args
		self.regs = vm.regs
		self.memory_size = mem_size
		self.length = len(str(hex(mem_size)))

	def _print_memory(self):
		'''Prints the content of each address of the VM's memory, if prints
		an asociation between the address as hexadecimal, and the location
		value as binary string'''

		for i, itm in enumerate(self.mem):
			print str(hex(i)).zfill(self.length), ' : ', itm

	def _print_amv(self):
		'''Prints the content of each variable defined in the VM, its type,
		its address and its value in binary, withous the occupation bit
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

		for itm in self.args.items:
			table.append([itm])

		print tabulate(table)

	def _print_regs(self):
		'''Prints the address of each register in the VM hardware, the address
		is the position in memeory that has the value pointed by the register
		'''

		table = []

		for name in self.regs:
			table.append([name.upper(), self.regs[name].zfill(self.length)])

		print tabulate(table)

	def _execute(self, command):
		'''Specifies the logif for each self.COMMAND variable'''

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

	def run(self):
		'''Receive the command and executes it as properly defined by
		self._execute. It should be called by the client code'''

		command = raw_input(self.INPUT_PROMPT)
		command = command.lower()

		while command != self.COMMANDS[4]:
			self._execute(command)

			command = raw_input(self.INPUT_PROMPT)
			command = command.lower()