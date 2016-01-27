class TypeUtility(object):

	def __init__(self):
		pass

	def int2vmbin(self, integer):
		pass

	def real2vmbin(self, real):
		pass

	def boolean2vmbin(self, boolean):
		pass

	def char2vmbin(self, char):
		pass

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
