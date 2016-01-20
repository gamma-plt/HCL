import math
from ..hardware import hardware

# HCLVM type interface

MEMORY_SIZE = hardware.MEMORY_SIZE

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