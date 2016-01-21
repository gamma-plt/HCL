import info

'''The atomic standard library, defines the set of native VM functions,
for a function to be added to the standard, it has to receive and return
just values of the type 'INTEGER', 'REAL', 'BOOLEAN', 'CHAR'. This is
why it's called atomic. To specify a function, it has to have an 
implementation in Python and a definition in TYPES, specifying the 
posiible argument tuple type, and return type'''

DEBUGGING = info.DEBUGGING


'''Allowed atomic types by the VM'''
ATOMIC_TYPES = ['INTEGER', 'REAL', 'BOOLEAN', 'CHAR']

# FUNCTIONS

def atomic_min(arg1, arg2):
	return arg2 if agr2 < arg1 else agr1

def atomic_max(arg1, arg2):
	return arg1 if agr2 < arg1 else agr2

def atomic_abs(arg):
	return 0 - arg if arg < 0 else arg

# TYPES
'''The type must be specified as a association to the function, as a tuple
of this form ((t1, [t2, ]), tn) where tn is the type of the returned value
by the function, and t1, t2, .., are the types of the arguments.

For example, the function add3, defined un Python as:

def and3(a, b, c):
	return a and b and c

Has a VM type: (('BOOLEAN', 'BOOLEAN', 'BOOLEAN',), 'BOOLEAN')

The tuple must be in a list which is the value of the function's name key
in the dictionary. If the function is polymorphic, one should include the
possible combinations of types'''

TYPES = {

	atomic_min : [((_, _), _) for _ in [ATOMIC_TYPES[0], ATOMIC_TYPES[1], ATOMIC_TYPES[3]]],
	atomic_max : [((_, _), _) for _ in [ATOMIC_TYPES[0], ATOMIC_TYPES[1], ATOMIC_TYPES[3]]],
	atomic_abs : [((ATOMIC_TYPES[0], ), (ATOMIC_TYPES[0])), ((ATOMIC_TYPES[1], ), (ATOMIC_TYPES[1]))],

}

def debugging():
	print TYPES

if DEBUGGING:
	debugging()