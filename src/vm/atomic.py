import info
import random

'''The atomic standard library, defines the set of native VM functions.
for a function to be added to the standard, it has to receive and return
just values of the type 'INTEGER', 'BOOLEAN', 'CHAR'. This is
why it's called atomic. To specify a function, it has to have an 
implementation in Python and a definition in TYPES, specifying the 
possible argument tuple type, and return type'''

DEBUGGING = info.DEBUGGING

'''Allowed atomic types by the VM'''
ATOMIC_TYPES = ['INTEGER', 'CHAR', 'BOOLEAN']

# TYPES
'''The type must be specified as a association to the function, as a tuple
of this form ((t1, {t2, }*), tn) where tn is the type of the returned value
by the function, and t1, t2, .., are the types of the arguments.

For example, the function and3, defined un Python as:

def and3(a, b, c):
	return a and b and c

Has a VM type: (('BOOLEAN', 'BOOLEAN', 'BOOLEAN',), 'BOOLEAN')

The tuple must be in a list which is the value of the function's name key
in the dictionary. If the function is polymorphic, one should include the
possible combinations of types'''

TYPES = {}

# FUNCTIONS
'''Functions are defined using a general argument, which is a dictionary
associating the number of the variable, for example 'arg1', 'arg2' with
the given value. Inside the functions, one should specify the specific
behavior of the function'''

# Defines the absolute value of an integer
def atomic_abs(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return 0 - arg1 if arg1 < 0 else arg1

	return innerfn(arg1)

TYPES[atomic_abs] = [((ATOMIC_TYPES[0], ), (ATOMIC_TYPES[0])),]

# ASCII representation of a number
def atomic_chr(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return chr(arg1) if arg1 in range(0, 128) else None

	return innerfn(arg1)

TYPES[atomic_chr] = [((ATOMIC_TYPES[0], ), (ATOMIC_TYPES[1])),]

# Tells if the given number is even
def atomic_evn(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1 % 2 == 0

	return innerfn(arg1)

TYPES[atomic_evn] = [((ATOMIC_TYPES[0], ), (ATOMIC_TYPES[2])),]

# Tells if the given character is alphanumeric
def atomic_isalnum(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1.isalnum()

	return innerfn(arg1)

TYPES[atomic_isalnum] = [((ATOMIC_TYPES[1], ), (ATOMIC_TYPES[2])),]

# Tells if the given character is alphabetic
def atomic_isalpha(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1.isalpha()

	return innerfn(arg1)

TYPES[atomic_isalpha] = [((ATOMIC_TYPES[1], ), (ATOMIC_TYPES[2])),]

# Tells if the given character is a digit
def atomic_isdigit(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1.isdigit()

	return innerfn(arg1)

TYPES[atomic_isdigit] = [((ATOMIC_TYPES[1], ), (ATOMIC_TYPES[2])),]

# Tells if the given character is lowercase
def atomic_islower(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1.islower()

	return innerfn(arg1)

TYPES[atomic_islower] = [((ATOMIC_TYPES[1], ), (ATOMIC_TYPES[2])),]

# Tells if the given character is an space
def atomic_isspace(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1.isspace()

	return innerfn(arg1)

TYPES[atomic_isspace] = [((ATOMIC_TYPES[1], ), (ATOMIC_TYPES[2])),]

# Tells if the given character is uppercase
def atomic_isupper(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1.isupper()

	return innerfn(arg1)

TYPES[atomic_isupper] = [((ATOMIC_TYPES[1], ), (ATOMIC_TYPES[2])),]

# The maximum of two numbers, or two characters
def atomic_max(args):
	arg1 = args['arg1']
	arg2 = args['arg2']

	def innerfn(arg1, arg2):
		return arg1 if arg2 < arg1 else arg2

	return innerfn(arg1, arg2)

TYPES[atomic_max] = [((_, _), _) for _ in [ATOMIC_TYPES[0], ATOMIC_TYPES[1]]]

# The minimum of two numbers, or two characters
def atomic_min(args):
	arg1 = args['arg1']
	arg2 = args['arg2']

	def innerfn(arg1, arg2):
		return arg2 if arg2 < arg1 else arg1

	return innerfn(arg1, arg2)

TYPES[atomic_min] = [((_, _), _) for _ in [ATOMIC_TYPES[0], ATOMIC_TYPES[1]]]

# Tells if the given number is odd
def atomic_odd(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1 % 2 != 0

	return innerfn(arg1)

TYPES[atomic_odd] = [((ATOMIC_TYPES[0], ), (ATOMIC_TYPES[2])),]

# Numeric representation of ASCII
def atomic_ord(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return ord(arg1) if ord(arg1) in range(0, 128) else None

	return innerfn(arg1)

TYPES[atomic_ord] = [((ATOMIC_TYPES[0], ), (ATOMIC_TYPES[1])),]

# Power function 
def atomic_pow(args):
	arg1 = args['arg1']
	arg2 = args['arg2']

	def innerfn(arg1, arg2):
		return arg1 ** arg2

	return innerfn(arg2, arg1)

TYPES[atomic_pow] = [((ATOMIC_TYPES[0], ATOMIC_TYPES[0]), (ATOMIC_TYPES[0])),]

# Predecessor of a number 
def atomic_pred(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1 - 1

	return innerfn(arg1)

TYPES[atomic_pred] = [((ATOMIC_TYPES[0], ), (ATOMIC_TYPES[0]))]

# Random integer between two given numbers
def atomic_rand(args):
	arg1 = args['arg1']
	arg2 = args['arg2']

	def innerfn(arg1, arg2):
		return random.randint(arg1, arg2)

	return innerfn(arg2, arg1)

TYPES[atomic_rand] = [((ATOMIC_TYPES[0], ATOMIC_TYPES[0]), (ATOMIC_TYPES[0])),]

# Successor of a number 
def atomic_succ(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1 + 1

	return innerfn(arg1)

TYPES[atomic_succ] = [((ATOMIC_TYPES[0], ), (ATOMIC_TYPES[0]))]

# Char to lowercase
def atomic_tolower(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1.lower()

	return innerfn(arg1)

TYPES[atomic_tolower] = [((ATOMIC_TYPES[1], ), (ATOMIC_TYPES[1])),]

# Char to uppercase
def atomic_toupper(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return arg1.upper()

	return innerfn(arg1)

TYPES[atomic_toupper] = [((ATOMIC_TYPES[1], ), (ATOMIC_TYPES[1])),]

def debugging():
	pass

if DEBUGGING:
	debugging()