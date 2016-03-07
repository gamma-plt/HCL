'''Set to True to turn on debugging mode.'''
DEBUGGING = False

def print_usage():
	print 'USAGE: vhcl <option> file_name'

def print_file_not_found(filename):
	print 'FILE NOT FOUND: ' + filename