import info

'''The atomic standard library, defines the set of native VM functions,
for a function to be added to the standard, it has to receive and return
just values of the type 'INTEGER', 'REAL', 'BOOLEAN', 'CHAR'. This is
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

TYPES = {

	atomic_min : [((_, _), _) for _ in [ATOMIC_TYPES[0], ATOMIC_TYPES[1]]],
	atomic_max : [((_, _), _) for _ in [ATOMIC_TYPES[0], ATOMIC_TYPES[1]]],
	atomic_abs : [((ATOMIC_TYPES[0], ), (ATOMIC_TYPES[0])),],

}

# FUNCTIONS
'''Functions are defined using a general argument, which is a dictionary
associating the number of the variable, for example 'arg1', 'arg2' with
the given value. Inside the functions, one should specify the specific
behavior of the function'''

# The minimum of two numbers, or two characters
def atomic_min(args):
	arg1 = args['arg1']
	arg2 = args['arg2']

	def innerfn(arg1, arg2):
		return arg2 if arg2 < arg1 else arg1

	return innerfn(arg1, arg2)

# The maximum of two numbers, or two characters
def atomic_max(args):
	arg1 = args['arg1']
	arg2 = args['arg2']

	def innerfn(arg1, arg2):
		return arg1 if arg2 < arg1 else arg2

	return innerfn(arg1, arg2)

# Defines the absolute value of an integer
def atomic_abs(args):
	arg1 = args['arg1']

	def innerfn(arg1):
		return 0 - arg1 if arg1 < 0 else arg1

	return innerfn(arg1)	

def debugging():
	pass

if DEBUGGING:
	debugging()