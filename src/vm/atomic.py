ATOMIC_TYPES = ['INTEGER', 'REAL', 'BOOLEAN', 'CHAR']

def atomic_min(arg1, arg2):
	return arg2 if agr2 < arg1 else agr1

def atomic_max(arg1, arg2):
	return arg1 if agr2 < arg1 else agr2

def atomic_abs(arg):
	return 0 - arg if arg < 0 else arg


types = {
	atomic_min : [(_, _) for _ in [ATOMIC_TYPES[0], ATOMIC_TYPES[1], ATOMIC_TYPES[3]]],
	atomic_max : [(_, _) for _ in [ATOMIC_TYPES[0], ATOMIC_TYPES[1], ATOMIC_TYPES[3]]],
	atomic_abs : [(ATOMIC_TYPES[0]), (ATOMIC_TYPES[1])]
}