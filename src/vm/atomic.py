def atomic_min(arg1, arg2):
	return arg2 if agr2 < arg1 else agr1

def atomic_max(arg1, arg2):
	return arg1 if agr2 < arg1 else agr2

types = {
	atomic_min : [(_, _) for _ in ['INTEGER', 'REAL', 'CHAR']],
	atomic_max : [(_, _) for _ in ['INTEGER', 'REAL', 'CHAR']]
}