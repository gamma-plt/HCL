from tabulate import tabulate

class Debugger(object):

	def __init__(self, mem, amv, args, world, mem_size):
		self.mem = mem
		self.amv = amv
		self.args = args
		self.world = world
		self.memory_size = mem_size
		self.length = len(str(hex(mem_size)))

	def print_memory(self):		
		for i, itm in enumerate(self.mem):
			print str(hex(i)).zfill(self.length), ' : ', itm

	def print_amv(self):
		table = []
		for itm in self.amv:
			packed = self.amv[itm]
			vm_type, vm_add = packed
			index = int(vm_add, 0)
			table.append([itm, vm_type, str(vm_add).zfill(self.length), self.mem[index]])
		print tabulate(table)

	def execute(self, command):
		if command == 'pmem':
			self.print_memory()

		elif command == 'pamv':
			self.print_amv()
