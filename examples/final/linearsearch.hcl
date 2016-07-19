program linearsearch
begin
	var n, i, target : int
	var low, upp, ans : int
	var a : array[0 .. 20] of int
	var newline, space : char
	newline ← "\n"
    space ← " "

	read(n)
	print newline
	low, upp, ans ← 0, 10, -1

	i  ← 0
	do i < n  → 
		a[i] ← rand(low, upp)
		i ← i + 1
	od

	i ← 0
	do i < n  → 
		print a[i]
		print space 
		i ← i + 1
	od

	print newline
	print newline
	read(target)
	print newline

	i  ← 0
	do i < n  → 
		if a[i] = target → 
			ans ← i
			i ← n
		fi
		i ← i + 1
	od

	print ans
	print newline

end
