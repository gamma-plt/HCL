import info
import types
import atomic
import debugger
import globalenv
import utilities

DEBUGGING = info.DEBUGGING
MEMORY_SIZE = globalenv.MEMORY_SIZE
WORD_SIZE = globalenv.WORD_SIZE

EMPTY_FLAG_BIT = '0'
OCCUP_FLAG_BIT = '1'
TYPES = ['INTEGER', 'BOOLEAN', 'CHAR']

def fetch_atomic_value(type_name, value):
	'''Returns the Python's value of some vm represented binary_string.
	It provides a bridge between the (type, value) tuples in the vm and 
	Python, is designed for operational facilities and compiler help'''

	obj = None

	# Does the type indicates, that value is an Integer?
	if type_name == TYPES[0]:
		obj = Integer(value)

	# Does the type indicates, that value is an Boolean?
	elif type_name == TYPES[1]:
		obj = Boolean(value)

	# Does the type indicates, that value is an Character?
	elif type_name == TYPES[2]:
		obj = Char(value)

	return obj.convert()

'''Defines the current functions in the enviroment, that is, the atomic
standard library'''
ATOMIC = {
	'min' : atomic.atomic_min,
	'max' : atomic.atomic_max,
	'abs' : atomic.atomic_abs	
}

# The sizes in words, required for the storage of a value of each type
TYPE_SIZE = {

	'INTEGER' : 1,
	'BOOLEAN' : 1,
	'CHAR' : 1

}

class Integer(object):
	'''The Integer class, represents the internal representation
	of the integer values in the HCL virtual machine. Integers
	are represented using two's complement. The maximum integer
	that can be represented in the VM, is defined by the parameters
	of the hardware operational descritption, that is MEMORY_SIZE.

	Bound checking and correct binary representation, must be done
	by the client code.

	Atributes:
		binrep : The binary string of the value to represent
	'''

	def __init__(self, binrep):
		'''Initializes an Integer object with the binary string given in binrep.
		binrep must be as in two's complement with the most significant bit meaning
		the sign of it'''

		self.sign = binrep[0]
		self.binrep = binrep[1:]

	def convert(self):
		'''Converts the object to a int value as understood by humans.
		It take into account the two's complement represetation of values'''

		power = 0
		ans = 0 - int(self.sign) * 2 ** (len(self.binrep))

		for bit in reversed(self.binrep):
			ans += (int(bit) * 2 ** power)
			power += 1

		return ans

class Real(object):
	'''The Real class, represents the internal representation
	of the real values in the HCL virtual machine. Real numbers
	are represented by the VM by splitting the integer and decimal
	parts of the number into two different memory locations. The
	maximum value that one can represent in the VM is given by
	the parameters of the hardware operational descritption, 
	that is MEMORY_SIZE. Since there are two different locations
	for each object, one can represent up to: Max(Integer).Max(Integer)

	Two illustrate better the approach to represent those numbers,
	one can check the following example:

	101.001 is:

	1 * 2^2  = 4
	0 * 2^1  = 0
	1 * 2^0  = 1
	.
	0 * 2^-1 = 0.0
	0 * 2^-2 = 0.0
	1 * 2^-3 = 0.125
	----------------
	101.001  = 5.125

	Bound checking and correct binary representation, must be done
	by the client code.

	Atributes:
		binrep_int : The binary string of the integer part of the number
		to be represented

		binrep_dec : The binary string of the decimal part of the number
		to be represented
	'''

	def __init__(self, binrep_int, binrep_dec):
		'''Initializes a Real object with the value given by binrep_int as
		the integer part and  binrep_dec as the decimal part. The sign is
		given by the two's complement representation ob binrep_int'''

		self.sign = binrep_int[0]
		self.binrep_int = binrep_int[1:]
		self.binrep_dec = binrep_dec

	def _convert_integer(self):
		'''Converts the integer part of the real number to an integer value
		as understood by humans. It take into account the two's complement 
		represetation of the integer part'''

		power = 0
		ans = 0 - int(self.sign) * 2 ** (len(self.binrep_int))

		for bit in reversed(self.binrep_int):
			ans += (int(bit) * 2 ** power)
			power += 1

		return ans

	def _convert_decimal(self):
		'''Converts the decimal part of the real number to a real value
		smaller than one and bigger or equal to zero as understood by humans'''

		power = 1
		ans = 0

		for bit in self.binrep_dec:
			ans += (int(bit) * 2 ** (0 - power))
			power += 1

		return ans

	def convert(self):
		'''Converts the object to a real value as understood by humans.
		It take into account the two's complement represetation of the
		binary representation of the integer part'''

		return self._convert_int() + self._convert_dec()

class Boolean(object):
	'''The Boolean class, represents the internal representation
	of the bool values in the HCL virtual machine. Booleans are
	represented using plain integers (not two's complment required).
	If the given binary string value is zero, it represent internally
	False, otherwise it is True

	Atributes:
		binrep : The binary string of the value to represent
	'''

	def __init__(self, binrep):
		'''Initializes a Boolean object with the binary string given in binrep.'''

		self.binrep = binrep

	def convert(self):
		'''Converts the object to a boolean value as understood by humans'''

		power = 0
		ans = 0

		for bit in reversed(self.binrep):
			ans += (int(bit) * 2 ** power)
			power += 1

		return False if ans == 0 else True 

class Char(object):
	'''The Char class, represents the internal representation
		of the char values in the HCL virtual machine. Characters are
		represented usng positive integers as in ASCII representation.
		The set of accepted and understood values of the ASCII charset
		is the one whose decimal values are in the range [32 .. 127].
		That is from ' ' to 'DEL'.

		Atributes:
			binrep : The binary string of the value to represent
	'''

	def __init__(self, binrep):
		'''Initializes a Char object with the binary string given in binrep.
		The binrep is given as in two's complement representation. If the 
		number represents a number out of the alowed range, the internal
		value of this Char object is NULL'''

		self.sign = binrep[0]
		self.binrep = binrep[1:]

	def convert(self):
		'''Converts the object to a char as being understood by humans.
		If self.binrep is out of the range, the value is converted to None'''

		power = 0
		ans = 0 - int(self.sign) * 2 ** (len(self.binrep))

		for bit in reversed(self.binrep):
			ans += (int(bit) * 2 ** power)
			power += 1

		return chr(ans) if ans in range(32, 128) else None

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

		{'summation' : ('BOOLEAN', '0x20')}

		self.args, represents the stack of arguments to be delivered to a function
		as defined in the atomic standard library of functions, the behavior of the
		VM related to the stack is defined by the user's (a compiler or a vhcl progrmmer)
		behavior. The values of this array consists of refrences to objects in the amv

		self.regs, defined an association between the registers of the self.world list
		and their current addresses. The user of the VM, must not name a variable with the
		same name of any of the registers, doing so, leads to undefined behavior. The value
		of each register is a pointer to the memory.
		'''

		self.memory = ['0' * (WORD_SIZE + 1) for i in range(MEMORY_SIZE)]
		self.amv = {}
		self.args = Stack()
		self.regs = {_ : 'NULL' for _ in self.world}

		for register in self.world[1:]:
			self.set_variable('.' + register + 'bol', 'BOOLEAN')
			self.set_variable('.' + register + 'int', 'INTEGER')
			self.set_variable('.' + register + 'chr', 'CHAR')

	def _value_of(self, address):
		address = int(address, 0)
		value = self.memory[address]
		value = value[1:]
		return value

	def _set_value(self, address, value):
		address = int(address, 0)
		self.memory[address] = value

	def _occupation_bit(self, word):
		'''Tells the occupation bit of any memory word'''

		return word[0]

	def _index_array(self, indexed_var):
		pass

	def _negate_occupation_bit(self, word):
		'''Sets the first bit of a word to the negation of it'''

		return '1' + word[1:] if word[0] == '0' else '0' + word[1:]

	def _alloc(self, words):
		'''Checks for memory available of the size of words to return the first address
		that satisfies such allocation requirements. This method, sets up the number of
		required word to occuppied bits in memory. If this variable is set up to
		MEMORY_SIZE, and words != MEMORY_SIZE, the allocations fails due to no memory
		available of such size. Boundary checks and error reports dependends on clients
		code.

		returns:
			current_address, the first adress in memory that satisfies that:
				*(mem + current_address) ... *(mem + current_address + words)
				was not occupied.
		'''

		i = 0
		current_size = 0
		current_address = 0

		while i < MEMORY_SIZE:
			prev_word = self.memory[i - 1]
			curr_word = self.memory[i]
			prev_occupation_bit = self._occupation_bit(prev_word)
			curr_occupation_bit = self._occupation_bit(curr_word)

			if prev_occupation_bit == OCCUP_FLAG_BIT and \
					curr_occupation_bit == EMPTY_FLAG_BIT:
				current_address = i
				current_size = 1

			elif curr_occupation_bit == EMPTY_FLAG_BIT:
				current_size += 1

			if current_size == words:
				break

			i += 1

		if current_size == MEMORY_SIZE:
			return -1

		return current_address

	def _allocate(self, first_address, words):
		'''Reseves memory for any purpose of words number of words beginning
		from the first_address, it is suppossed that was previously checked
		that the memory was available. It must be used after a call of self.alloc
		with the first_address as the result of it.
		'''

		i = first_address
		chunks = 0

		while chunks != words:
			curr_word = self.memory[i] 
			self.memory[i] = self._negate_occupation_bit(curr_word)
			i += 1
			chunks += 1

	def _sizeof(self, name, variable=False):
		'''Returns the words occupied by a type, or a variable (if variable)'''

		if variable:
			return self._sizeof_variable(name)
		else:
			return self._sizeof_type(name)

	def _sizeof_variable(self, variable):
		'''Returns the size of words required by some variable in the amv'''

		var_type, var_addr = self.amv[variable]
		ans = 0
		if var_type in TYPE_SIZE:
			ans = TYPE_SIZE[var_type]
		else:
			ans = utilities.compound_sizeof(var_type)

		return ans

	def _sizeof_type(self, type_name):
		'''Returns the size of words required by some type'''

		ans = 0
		if type_name in TYPE_SIZE:
			ans = TYPE_SIZE[type_name]
		else:
			ans = utilities.compound_sizeof(type_name)

		return ans

	def _fn_handler(self, args):
		'''Returns the value of '''
		args_package = {}
		string = 'arg'
		i = 1
		for itm_type, itm_address in args:
			binary_value = self._value_of(itm_address)
			real_value = fetch_atomic_value(itm_type, binary_value)
			arg_name = string + str(i)
			args_package[arg_name] = real_value			
			i += 1

		return args_package

	def _set(self, var_name, var_type):
		'''Adds a new entry (or modifies one if not properly used) to self.amv
		associating var_name with its given type and the address found for it,
		it returns the adress of the new variable if the memory has free memory
		for it, otherwise, if returns -1
		'''

		sizeof_var = self._sizeof(var_type)
		address = self._alloc(sizeof_var)

		if address == -1:
			self.regs['add'] = hex(0)
			return -1
		else:
			self._allocate(address, sizeof_var)
			self.amv[var_name] = (var_type, hex(address))
			self.regs['add'] = hex(address)
			return address

	def _mov(self, variable, operator):
		isvalue = utilities.isbinarystring(operator)
		_, mem_address1 = self.amv[variable]
		value = None

		if isvalue:
			value = operator

		else:			
			_, mem_address2 = self.amv[operator]
			value = self._value_of(mem_address2)

		value = '1' + value.zfill(WORD_SIZE)		
		self._set_value(mem_address1, value)

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

	def free(self, variable):
		'''Sets to unocuppied the memory location of variable, the variable
		must be allocated, must be in amv. If not, the behavior is undefined.
		Those checks are responsability of the client's code. After its execution,
		there chunks occuppied by variable are now free. And the variable is
		removed from the amv, and the memory
		'''

		var_type, var_addr = self.amv[variable]
		size_of = self._sizeof(variable, True)

		i = int(var_addr, 0)
		free_chunks = 0

		while free_chunks != size_of:
			curr_word = self.memory[i] 
			self.memory[i] = self._negate_occupation_bit(curr_word)

			free_chunks += 1
			i += 1

		self.amv.pop(variable)

	def set_variable(self, var_name, var_type):
		'''Adds a new entry (or modifies one if not properly used) to self.amv
		associating var_name with its given type and the address found for it,
		it returns the adress of the new variable if the memory has free memory
		for it, otherwise, if returns -1
		'''

		sizeof_var = self._sizeof(var_type)
		address = self._alloc(sizeof_var)

		if address == -1:
			self.regs['add'] = hex(0)
			return -1
		else:
			self._allocate(address, sizeof_var)
			self.amv[var_name] = (var_type, hex(address))
			self.regs['add'] = hex(address)
			return address

	def push_argument(self, argument):
		isvalue = utilities.isbinarystring(argument)
		isvariable = not isvalue

		if isvalue:
			print 'Trying to push a value'
			return

		else:

			if argument in self.amv:
				type_name, address = self.amv[argument] 
				value = self.memory[int(address, 0)]
				self.args.push((type_name, address))

			else:
				return False

		return True

	def call_function(self, name):
		if name in ATOMIC:
			fn_type = atomic.TYPES[ATOMIC[name]]
			arg_arity = len(fn_type[0][0])

			i = 0
			arguments = []

			while i < arg_arity:
				arguments.append(self.args.pop())
				i += 1

			arguments = self._fn_handler(arguments)
			fn_result = ATOMIC[name]
			result = fn_result(arguments)

			return result

		else:
			return False

def debugging():

	vm = HCLVirtualMachine()
	db = debugger.Debugger(vm, MEMORY_SIZE)
	db.run()

if DEBUGGING:
	debugging()