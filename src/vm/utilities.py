class TypeUtility(object):

	def __init__(self, word_size):
		self.word_size = word_size

	def int2vmbin(self, integer):
		sign = '1' if integer < 0 else '0'
		bitstring = ''
		integer = abs(integer)

		while integer > 0:
			bit = integer % 2
			quotient = integer / 2
			bitstring = str(bit) + bitstring
			integer = quotient

		return sign + bitstring.zfill(self.word_size - 1)

	def real2vmbin(self, real):
		pass

	def boolean2vmbin(self, boolean):
		return self.int2vmbin(1) if boolean else self.int2vmbin(0)

	def char2vmbin(self, char):
		vmascii = ord(char)

		if vmascii in range(32, 128):
			return self.int2vmbin(vmascii)
		else:
			return self.int2vmbin(0)

def isbinarystring(string):
	for ch in string:
		if ch not in ['0', '1']:
			return False
	return True

def compound_sizeof(type_name):
	value = 0
	chunks = 0

	if '#' in type_name:
		idx = type_name.index('#')
		value = type_name[idx + 1:]
		chunks = 1

		if '#' in value:
			value, chunks = value.split('#')

	return int(value) * int(chunks)