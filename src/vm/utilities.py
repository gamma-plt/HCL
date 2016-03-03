class TypeUtility(object):

	def __init__(self, word_size):
		self.word_size = word_size

	def int2vmbin(self, integer):

		if integer < 0:
			integer = (1 << self.word_size) + integer

		formatstring = '{:0%ib}' % self.word_size

		return formatstring.format(integer)

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

def isarrayvariable(variable):
	indexes = [variable.count('['), variable.count(']')]
	if indexes[0] == 1 and indexes[1] == 1:
		return True, 1
	elif indexes[0] == 2 and indexes[1] == 2:
		return True, 2
	return False, -1

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