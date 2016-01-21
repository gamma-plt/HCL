import info
import atomic
import debugger

DEBUGGING = info.DEBUGGING

'''Defines the words of the memory.'''
MEMORY_SIZE = 34

'''Defines the number of bits for each word.
This must not take into account the occupation bit.
That its a flag to indicates wheter or not the word
is occuppied'''
WORD_SIZE = 16

ATOMIC = {
	'min' : atomic.atomic_min,
	'max' : atomic.atomic_max,
	'abs' : atomic.atomic_abs	
}

def atomic_args(name):
	pass

class Stack(object):
	'''Defines a linear data structure known as the stack, it usage
	is for the stack of variables used in the VM, it has the normal
	operational methods of any stack defined in a standard data
	structures and algorithms book
	'''

	def __init__(self):
		'''Initializes an Stack object, it is internally represented
		as a native Python's list, the set of operations are restricted
		'''

		self.items = []

	def is_empty(self):
		'''Tells wheter or not the stack is empty'''

		return self.items == []

	def push(self, item):
		'''Pushes a value on the stack'''

		self.items.append(item)

	def pop(self):
		'''Returns the upper value on the stack, and removes it from
		the same'''

		return self.items.pop()

	def size(self):
		'''Returns the number of items allocated in the stack'''

		return len(self.items)

class HCLVirtualMachine(object):
	'''Defines an instance of an HCLVM, it provides the structure,
	organization and execution of a HCLVM as defined in the documents.
	Aside from the structure, and organization, it defines the data storage,
	command execution and data representation.

	Every HCLVM has a memory, a table of variables, a stack of arguments
	and a set of registers
	'''

	'''The world is the set of elements that are present at initialization
	as registers'''
	world = ['add', 'ret', 'r1', 'r2', 'r3', 'r4', 'r5']

	def __init__(self):
		'''Initializes an instance of the class.

		self.memory, represents the memory as in RAM of the vm. The memory
		is where all the data are allocated using bits, the interpretation
		of each bit depends on the type of each register, the conversion and
		data interpretation process depends on the client code.

		self.amv, represents an associative memory of variables, that associates
		the name of each variable with its type (for internal representation), and
		its address as in hexadecimal in the memory of the VM. The form of the
		association is exemplified:

		{'summation' : ('BOOL', '0x20')}

		self.args, represents the stack of arguments to be delivered to a function
		as defined in the atomic standard library of functions, the behavior of the
		VM related to the stack is defined by the user's (a compiler or a vhcl progrmmer)
		behavior.

		self.regs, defined an association between the registers of the self.world list
		and their current addresses. The user of the VM, must not name a variable with the
		same name of any of the registers, doing so, leads to undefined behavior.
		'''

		self.memory = ['0' * (WORD_SIZE + 1) for i in range(MEMORY_SIZE)]
		self.amv = {}
		self.args = Stack()
		self.regs = {_ : 'NULL' for _ in self.world}

	def alloc(self, words):
		pass

def debugging():
	vm = HCLVirtualMachine()
	db = debugger.Debugger(vm, MEMORY_SIZE)
	db.run()

if DEBUGGING:
	debugging()