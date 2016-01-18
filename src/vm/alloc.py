memory = ['110101010', '111010100', '110101010', '110101010'] * 10
size = len(memory)

def convert(bin_string):
	if len(bin_string) == 8:
		rep = int(bin_string, 2)

		if rep in range(230):
			return rep

		else:
			return chr(rep - 133)

def CEX(a, b):
	if a < 0 or a >= size:
		print 'Overflow'
	elif b < 0 or b >= size:
		print 'Overflow'
	else:
		a, b = min(a, b), max(a, b)
		if memory[a] > memory[b]:
			temp = memory[a]
			memory[a] = memory[b]
			memory[b] = temp

def print_memory():
	for i, itm in enumerate(memory):
		print hex(i), ' : ', itm

def find_free(size, mem = memory):
	ans = None
	flag = True
	if(size == 0):
		flag = False

	length = 0
	curr = 0
	ans = None

	while curr < len(mem) and flag:
		if mem[curr] == None:
			ans = None if ans != None else curr
			length = length + 1
		else:
			ans = curr
			length = 0

		if length == size:
			flag = False

		curr = curr + 1

	return ans - size + 1

def main():
	
	while True:
		instruction = raw_input()
		parse = instruction.split()

		if len(parse) >= 1:
			command = parse[0]

			if command == 'CEX':
				CEX(int(parse[1], 16), int(parse[2], 16))

			elif command == 'MEM':
				print_memory()

			elif command == 'MOV':
				first_address = parse[1]
				value = parse[2]

				memory[int(first_address, 16)] = value

			elif command == 'QUIT':
				break


if __name__ == '__main__':
	#main()

	print_memory()