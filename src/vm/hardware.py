import sys
import info
import types
import random
import atomic
import debugger
import globalenv
import utilities

QUITTER = False
DEBUGGING = info.DEBUGGING
MEMORY_SIZE = globalenv.MEMORY_SIZE
WORD_SIZE = globalenv.WORD_SIZE

EMPTY_FLAG_BIT = '0'
OCCUP_FLAG_BIT = '1'
TYPES = ['INTEGER', 'BOOLEAN', 'CHAR']

'''Defines the current functions in the enviroment, that is, the atomic
standard library'''
ATOMIC = {
	'abs' : atomic.atomic_abs,
	'chr' : atomic.atomic_chr,
	'even' : atomic.atomic_evn,
	'isalnum' : atomic.atomic_isalnum,
	'isalpha' : atomic.atomic_isalpha,
	'isdigit' : atomic.atomic_isdigit,
	'islower' : atomic.atomic_islower,
	'isspace' : atomic.atomic_isspace,
	'isupper' : atomic.atomic_isupper,
	'max' : atomic.atomic_max,
	'min' : atomic.atomic_min,
	'odd' : atomic.atomic_odd,
	'ord' : atomic.atomic_ord,	
	'pow' : atomic.atomic_pow,
	'pred' : atomic.atomic_pred,
	'rand' : atomic.atomic_rand,
	'succ' : atomic.atomic_succ, 
	'tolower' : atomic.atomic_tolower, 
	'toupper' : atomic.atomic_toupper, 
}

# The sizes in words, required for the storage of a value of each type
TYPE_SIZE = {
	'INTEGER' : 1,
	'BOOLEAN' : 1,
	'CHAR' : 1
}

MANAGER = utilities.TypeUtility(WORD_SIZE)

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

		return chr(ans) if ans in range(0, 128) else None

def fetch_atomic_value(type_name, value):
	'''Returns the Python's value of some vm represented binary_string.
	It provides a bridge between the (type, value) tuples in the vm and 
	Python, is designed for operational facilities and compiler help'''

	obj = 'NULL'

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
	WORLD = ['add', 'ret', 'r1', 'r2', 'r3', 'r4', 'r5']

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
		self.regs = {_ : 'NULL' for _ in self.WORLD}

		self._binary_instructions = {
										'mov' : self._mov, 'and' : self._and, 
										'or' : self._or, 'xor' : self._xor, 
										'add' : self._add, 'sub' : self._sub, 
										'mul' : self._mul, 'div' : self._div, 
										'mod' : self._mod, 'cmp' : self._cmp
									}
		

		self._unary_instructions = {
										'not' : self._not, 'dec' : self._dec, 
										'inc' : self._inc, 'push' : self._push, 
										'call' : self._call, 'free' : self._free, 
										'print' : self._print, 'readint' : self._readint,
										'readchr' : self._readchr
									}
		
		self.flags = {
						'equ' : False, 'slt' : False, 'sgt' : False, 
						'leq' : False, 'geq' : False, 'neq' : False
					}

		for register in self.WORLD[2:]:
			self._set('.' + register + 'bol', 'BOOLEAN')
			self._set('.' + register + 'int', 'INTEGER')
			self._set('.' + register + 'chr', 'CHAR')

		self._set('..retint', 'INTEGER')
		self._set('..retchr', 'CHAR')
		self._set('..retbol', 'BOOLEAN')

		self._set('..infty_pos', 'INTEGER')
		self._mov('..infty_pos', '0' + ('1' * (WORD_SIZE - 1)))
		self._set('..infty_neg', 'INTEGER')
		self._mov('..infty_neg', '1' + ('0' * (WORD_SIZE - 1)))

	def _fetch(self, variable):
		'''Returns the type and arress of the variable given by parameter, if variable points
		to a not-structured data, it returns the address that stores the value pointed
		by variable. If it's a 1-dimensional array, it treats variable as var_name[num]
		and returns the address of var_name[num]. If it's a 2-dimensinonal array, the
		function treats variable as var_name[i][j], and returns the address of it. Address
		conversion is independent from this function, it uses self._index() instead. If the
		given parameter is not a variable but a value, it returns \'NULL\''''
		
		atomic_type, address = '', ''
		isarray, dimension = utilities.isarrayvariable(variable)

		if isarray:

			min_bound = variable.index('[')
			max_bound = variable.index(']')
			var_name =  variable[:min_bound]
			try:
				atomic_type, _ = self.amv[var_name]
				atomic_type = atomic_type[:atomic_type.index('#')]
			except:
				# No existe ese arreglo
				print 'ERROR: VAR002_ERROR', var_name
				if QUITTER: 
					quit()
				else:
					return False, False

			if dimension == 1:
				
				index = variable[min_bound + 1 : max_bound]
				address = self._index(var_name, index)				

			elif dimension == 2:

				rows = variable[min_bound + 1 : max_bound]
				scnd_index = variable[max_bound + 1:]
				min_bound = scnd_index.index('[')
				max_bound = scnd_index.index(']')
				cols = scnd_index[min_bound + 1 : max_bound]
				address = self._index(var_name, rows, cols)

		else:
			isvalue = utilities.isbinarystring(variable)
			if isvalue:
				atomic_type = 'NULL'
				address = 'NULL'

			else:
				
				try:
					atomic_type, address = self.amv[variable]
				except:
					# No existe la variable
					print 'ERROR: VAR001_ERROR', variable
					if QUITTER: 
						quit()
					else:
						return False, False

		return atomic_type, address

	def _value_of(self, address):
		'''Returns the binary value stored at address, it just removes the occupation
		bit.'''

		address = int(address, 0)

		try:
			value = self.memory[address]
			value = value[1:]
			return value
		except:
			print 'ERROR: MEM002_ERROR'		

	def _set_value(self, address, value):
		'''It stores the given value in binary at the given address'''

		address = int(address, 0)
		#value = value[:WORD_SIZE + 1]
		self.memory[address] = value[:WORD_SIZE + 1]

	def _occupation_bit(self, word):
		'''Tells the occupation bit of any memory word'''

		return word[0]

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

			if i == len(self.memory):
				print 'ERROR: MEM001_ERROR'
				if QUITTER: 
					quit()
				else:
					return

			curr_word = self.memory[i] 
			self.memory[i] = self._negate_occupation_bit(curr_word)
			i += 1
			chunks += 1

	def _index_array(self, variable_name, index):
		_type, _address = self.amv[variable_name]
		_type, length = _type.split('#')
		_address = int(_address, 0)

		return hex(_address + index)

	def _index_matrix(self, variable_name, i, j):
		_type, _address = self.amv[variable_name]
		_type, length1, length2 = _type.split('#')

		base = int(hex(int(_address, 0) + int(length2) * i), 0)
		base += j

		return hex(base)

	def _index(self, variable_name, i, j=-1):
		'''Retrieves the address of the value pointed by variable_name at the given index.
		The array might be pointed by variable_name, and the returned value, is
		the address of variable_name[index1]. If index2 != -1, then, we treat
		the array as a matrix, and the returned value is the address of 
		variable_name[index1][index2]
		'''

		i = str(i)

		if not(i.isdigit()):
			_, add = self._fetch(i)
			if _ == False: return
			value = self._value_of(add)
			i = Integer(value).convert()

		if j == -1:
			return self._index_array(variable_name, int(i))

		else:
			j = str(j)

			if not(j.isdigit()):
				_, add = self._fetch(j)
				if _ == False: return
				value = self._value_of(add)
				j = Integer(value).convert()

			return self._index_matrix(variable_name, int(i), int(j))

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

	def _get_binary_pair(self, variable, operator):
		isvalue = utilities.isbinarystring(operator)
		_, mem_address1 = self._fetch(variable)
		if _ == False: return
		val1 = self._value_of(mem_address1)
		val2 = ''

		if isvalue:
			val2 = operator

		else:			
			_, mem_address2 = self._fetch(operator)
			if _ == False: return
			val2 = self._value_of(mem_address2)

		val1 = val1.zfill(WORD_SIZE)
		val2 = val2.zfill(WORD_SIZE)

		return val1, val2, mem_address1

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

		types = ['integer', 'char', 'boolean']

		if var_type.split('#')[0] not in types + map(lambda x : x.upper(), types):
			print 'ERROR: TYPE001_ERROR'
			if QUITTER: 
				quit()
			else:
				return False

		var_type = var_type.upper()

		sizeof_var = self._sizeof(var_type)
		address = self._alloc(sizeof_var)

		if address == -1:
			self.regs['add'] = hex(0)
			return -1
		else:
			self._allocate(address, sizeof_var)
			self.amv[var_name] = (var_type.upper(), hex(address))
			self.regs['add'] = hex(address)
			return address

	def _mov(self, variable, operator):
		isvalue = utilities.isbinarystring(operator)
		_, mem_address1 = self._fetch(variable)
		if _ == False: return
		value = None

		if isvalue:
			value = operator		

		else:			
			_, mem_address2 = self._fetch(operator)
			if _ == False: return
			value = self._value_of(mem_address2)

		value = '1' + value.zfill(WORD_SIZE)		
		self._set_value(mem_address1, value)

	def _not(self, variable):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of negate a whole binary string, which is the value
		of the given variable'''

		try:
			_, mem_address = self._fetch(variable)
			if _ == False: return

			value = self._value_of(mem_address)
			value = ''.join(['0' if bit == '1' else '1' for bit in value])

			value = '1' + value.zfill(WORD_SIZE)		
			self._set_value(mem_address, value)

		except:
			print 'ERROR: VAR001_ERROR', variable
			if QUITTER: 
				quit()
			else:
				return


	def _and(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of get the logical and of the variable's value and the
		given operator's value'''
		
		val1, val2, mem_address1 = self._get_binary_pair(variable, operator)

		val = ''
		i = 0

		while i < WORD_SIZE:
			val += '1' if val1[i] == val2[i] == '1' else '0'
			i += 1

		val = '1' + val.zfill(WORD_SIZE)		
		self._set_value(mem_address1, val)

	def _or(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of get the logical or of the variable's value and the
		given operator's value'''
		
		val1, val2, mem_address1 = self._get_binary_pair(variable, operator)

		val = ''
		i = 0

		while i < WORD_SIZE:
			val += '1' if (val1[i] == '1' or val2[i] == '1') else '0'
			i += 1
			
		val = '1' + val.zfill(WORD_SIZE)
		self._set_value(mem_address1, val)

	def _xor(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of get the logical xor of the variable's value and the
		given operator's value'''
		
		val1, val2, mem_address1 = self._get_binary_pair(variable, operator)

		val = ''
		i = 0

		while i < WORD_SIZE:
			val += '1' if (val1[i] != val2[i]) else '0'
			i += 1
			
		val = '1' + val.zfill(WORD_SIZE)
		self._set_value(mem_address1, val)

	def _add(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of adding the the value of the variable and the 
		operator's value'''
		
		val1, val2, mem_address1 = self._get_binary_pair(variable, operator)

		val1 = Integer(val1).convert()
		val2 = Integer(val2).convert()

		val = MANAGER.int2vmbin(val1 + val2)
			
		val = '1' + val.zfill(WORD_SIZE)
		self._set_value(mem_address1, val)

	def _sub(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of substract the the value of the variable and the 
		operator's value'''
		
		val1, val2, mem_address1 = self._get_binary_pair(variable, operator)

		val1 = Integer(val1).convert()
		val2 = Integer(val2).convert()

		val = MANAGER.int2vmbin(val1 - val2)
			
		val = '1' + val.zfill(WORD_SIZE)
		self._set_value(mem_address1, val)

	def _inc(self, variable):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of incrementing in one the value of some binary_string,
		which is the value of the given variable passed as argument'''
		
		self._add(variable, ('0' * (WORD_SIZE - 1)) + '1')

	def _dec(self, variable):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of decrementing in one the value of some binary_string,
		which is the value of the given variable passed as argument'''
		
		self._sub(variable, ('0' * (WORD_SIZE - 1)) + '1')

	def _mul(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of multiply the the value of the variable and the 
		operator's value'''
		
		val1, val2, mem_address1 = self._get_binary_pair(variable, operator)

		val1 = Integer(val1).convert()
		val2 = Integer(val2).convert()

		val = MANAGER.int2vmbin(val1 * val2)
			
		val = '1' + val.zfill(WORD_SIZE)
		self._set_value(mem_address1, val)

	def _div(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of divide the the value of the variable and the 
		operator's value'''
		
		val1, val2, mem_address1 = self._get_binary_pair(variable, operator)

		val1 = Integer(val1).convert()
		val2 = Integer(val2).convert()

		val = MANAGER.int2vmbin(val1 / val2)
			
		val = '1' + val.zfill(WORD_SIZE)
		self._set_value(mem_address1, val)

	def _mod(self, variable, operator):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose to get the module of the the value of the variable 
		and the operator's value'''
		
		val1, val2, mem_address1 = self._get_binary_pair(variable, operator)

		val1 = Integer(val1).convert()
		val2 = Integer(val2).convert()

		val = MANAGER.int2vmbin(val1 % val2)
			
		val = '1' + val.zfill(WORD_SIZE)
		self._set_value(mem_address1, val)

	def _get_integer_values(self, operator1, operator2):
		val1 = ''
		type1 = ''
		isvalue = utilities.isbinarystring(operator1)
		if isvalue:
			val1 = operator1
		else:
			type1, mem_address = self._fetch(operator1)
			if type1 == False: return
			val1 = self._value_of(mem_address)

		val2 = ''
		type2 = ''
		isvalue = utilities.isbinarystring(operator2)
		if isvalue:
			val2 = operator2
		else:
			type2, mem_address = self._fetch(operator2)
			if type2 == False: return
			val2 = self._value_of(mem_address)

		val1 = val1.zfill(WORD_SIZE)
		val2 = val2.zfill(WORD_SIZE)

		val1 = Integer(val1).convert()
		val2 = Integer(val2).convert()

		return val1, val2

	def _cmp(self, operator1, operator2):

		val1, val2 = self._get_integer_values(operator1, operator2)

		self.flags['equ'] = val1 == val2
		self.flags['neq'] = val1 != val2
		self.flags['slt'] = val1 < val2
		self.flags['sgt'] = val1 > val2
		self.flags['leq'] = val1 <= val2
		self.flags['geq'] = val1 >= val2

	def _readint(self, variable):
		value = input()
		value = MANAGER.int2vmbin(value)
		
		self._mov(variable, value)

	def _readchr(self, variable):
		value = sys.stdin.read(1)
		value = MANAGER.char2vmbin(value[0])
		
		self._mov(variable, value)

	def _print(self, variable):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of printing the current value of some variable 
		allocated in the vm's memory'''
 
		isvalue = utilities.isbinarystring(variable)

		if isvalue:
			msg = Integer(variable).convert()

		elif variable[0] == variable[-1] == '"':
			msg = variable[1:-1]
			msg = msg.replace('_', ' ')

		else:

			type_name, mem_address = self._fetch(variable)
			if type_name == False: return
			value = self._value_of(mem_address)

			msg = fetch_atomic_value(type_name, value)

		sys.stdout.write(str(msg))

	def _push(self, argument):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of pushin some value or a variable's value to the
		vm arguments stack'''
		
		isvalue = utilities.isbinarystring(argument)

		if isvalue:
			print 'Trying to push a value'
			return

		else:

			type_name, address = self._fetch(argument)
			if type_name == False: return
			value = self.memory[int(address, 0)]
			self.args.push((type_name, address))

		return True

	def _call(self, name):
		'''Implements the logic for communicating between the debugger and the
		vm, for the purpose of calling a function, as defined in atomic library
		'''

		fnrgs = ['..retint', '..retchr', '..retbol']

		for fnrg in fnrgs:
			_, mem_address = self._fetch(fnrg)
			if _ == False: return
			self._set_value(mem_address, '1' + '0')
		
		if name in ATOMIC:
			fn_type = atomic.TYPES[ATOMIC[name]]
			arg_arity = len(fn_type[0][0])
			fn_type = dict(fn_type)

			i = 0
			arguments = []

			while i < arg_arity:
				arguments.append(self.args.pop())
				i += 1

			arguments_types = tuple([tp for tp, _ in arguments])

			if arguments_types in fn_type:
				return_type = fn_type[arguments_types]
				arguments = self._fn_handler(arguments)

				ret_rgs = {
							TYPES[0] : ('..retint', MANAGER.int2vmbin), 
							TYPES[1] : ('..retbol', MANAGER.boolean2vmbin), 
							TYPES[2] : ('..retchr', MANAGER.char2vmbin)
						}
				
				fn_result = ATOMIC[name]
				result = fn_result(arguments)

				if result:
					proper_register, conv_function = ret_rgs[return_type]
					_, mem_address = self._fetch(proper_register)
					if _ == False: return
					result = conv_function(result)
					
					self._set_value(mem_address, '1' + result)

				else:
					# Wrong types
					pass

				return result

			else:
				return False

		else:
			# Undeclared function
			print 'ERROR: CALL001_ERROR'
			if QUITTER: 
				quit()
			else:
				return

	def _free(self, variable):
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

	# Execution

	def _execute_binarycommand(self, command, args):
		self._binary_instructions[command](args[0], args[1])

	def _execute_unarycommand(self, command, args):
		self._unary_instructions[command](args[0])

	def _execute_gssinstruction(self, node):
		gss_instruction = node
		guards = gss_instruction.args
		for guard in guards:
			self._set(guard, 'BOOLEAN')
			self._mov(guard, '0000000')
		return guards

	def _filter_guards(self, guards):
		true_guards = []

		for guard in guards:
			guard_type, guard_address = self._fetch(guard)
			if guard_type == False: return
			guard_value = self._value_of(guard_address)
			guard_value = fetch_atomic_value(guard_type, guard_value)
			if guard_value:
				true_guards.append(guard)

		return true_guards

	def _free_guards(self, guards):
		for guard in guards:
			self._free(guard)

	def _execute_actinstruction(self, act_instructions, guards):
		true_guards = self._filter_guards(guards)

		if true_guards:
			true_guard = random.choice(true_guards)
			executed_block = filter(lambda instruction : instruction.args[0] == \
				true_guard, act_instructions).pop()

			for child in executed_block.children:
				self._execute_node(child)

		return true_guards

	def _execute_ifcommand(self, node):

		level = node.level
		line = node.line
		command = node.command
		args = map(lambda x : x.lower(), node.args)
		children = node.children

		gss_instruction = None
		act_instructions = []
		guards = []

		for child in children:
			if child.command == 'gss':
				guards = self._execute_gssinstruction(child)
			elif child.command == 'act':
				child.args = map(lambda x : x.replace(':', ''), child.args)
				act_instructions.append(child)
			else:
				self._execute_node(child)

		self._execute_actinstruction(act_instructions, guards)
		self._free_guards(guards)

	def _loop(self, clc_instruction, act_instructions, guards):
		for child in clc_instruction.children:
			self._execute_node(child)

		true_guards = self._execute_actinstruction(act_instructions, guards)

		while true_guards:

			for guard in guards:
				self._mov(guard, '0')

			for child in clc_instruction.children:
				self._execute_node(child)

			true_guards = self._execute_actinstruction(act_instructions, guards)				

	def _execute_docommand(self, node):
		
		level = node.level
		line = node.line
		command = node.command
		args = map(lambda x : x.lower(), node.args)
		children = node.children

		gss_instruction = None
		act_instructions = []
		guards = []

		for child in children:
			if child.command == 'gss':
				guards = self._execute_gssinstruction(child)
			elif child.command == 'act':
				child.args = map(lambda x : x.replace(':', ''), child.args)
				act_instructions.append(child)
			elif child.command == 'clc':
				clc_instruction = child

		self._loop(clc_instruction, act_instructions, guards)
		self._free_guards(guards)

	def _execute_node(self, node):

		level = node.level
		line = node.line
		command = node.command
		args = map(lambda x : x.lower(), node.args)
		children = node.children
		
		if command == 'set':
			var_name, var_type = args[0], args[1]
			association = {'integer' : 'INTEGER', 'boolean' : 'BOOLEAN', \
										'char' : 'CHAR'}

			if var_type in association:
				self._set(var_name, association[var_type])
			else:
				parse = var_type.split('#')
				if parse[0] in association:
					self._set(var_name, var_type)

		elif command in self._binary_instructions:
			self._execute_binarycommand(command, args)

		elif command in self._unary_instructions:
			self._execute_unarycommand(command, args)

		elif command in self.flags.keys():
			if self.flags[command]:
				for child in children:
					self._execute_node(child)

		elif command == 'do':
			self._execute_docommand(node)

		elif command == 'skip':
			pass

		elif command == 'if':
			self._execute_ifcommand(node)

		elif command == 'halt':
			
			if debugging:
				pass 
			else:
				if QUITTER: 
					quit()
				else:
					return

	def process_syntax_tree(self, syntax_tree):

		for node in syntax_tree:
			self._execute_node(node)

def debugging():

	vm = HCLVirtualMachine()

	db = debugger.Debugger(vm, MEMORY_SIZE)
	db.run()	

if DEBUGGING:
	debugging()
	pass