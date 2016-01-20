from tabulate import tabulate

class Debugger(object):

	def __init__(self, vm, mem_size):
		self.mem = vm.memory
		self.amv = vm.amv
		self.args = vm.args
		self.regs = vm.regs
		self.memory_size = mem_size
		self.length = len(str(hex(mem_size)))

	def _print_memory(self):		
		for i, itm in enumerate(self.mem):
			print str(hex(i)).zfill(self.length), ' : ', itm

	def _print_amv(self):
		table = []
		for itm in self.amv:
			packed = self.amv[itm]
			vm_type, vm_add = packed
			index = int(vm_add, 0)
			'''We remove the occupation bit'''
			vm_val = self.mem[index][1:]
			table.append([itm, vm_type, str(vm_add).zfill(self.length), vm_val])
		print tabulate(table)

	def _print_args(self):
		table = []
		for itm in self.args.items:
			table.append([itm])
		print tabulate(table)

	def _print_regs(self):
		table = []
		for name in self.regs:
			table.append([name.upper(), self.regs[name]])
		print tabulate(table)

	def _execute(self, command):
		if command == 'pmem':
			self._print_memory()

		elif command == 'pamv':
			self._print_amv()

		elif command == 'pstk':
			self._print_args()

		elif command == 'prgs':
			self._print_regs()

		else:
			print 'WRONG COMMAND'

	def run(self):
		command = raw_input('(cmd) ')
		command = command.lower()

		while command != 'quit':
			self._execute(command)

			command = raw_input('(cmd) ')
			command = command.lower()