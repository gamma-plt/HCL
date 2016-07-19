program bubblesort
begin
	var n, i, j, target : int
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

	var temp : int
	print newline

	i  ← 0
	do i < n  → 
		j  ← 1
		do j < n →
			if a[j - 1] > a[j] → 
				temp ← a[j]
				a[j] ← a[j - 1]
				a[j - 1] ← temp
			fi
			j ← j + 1
		od
		i ← i + 1
	od

	i ← 0
	do i < n  → 
		print a[i] 
		print space
		i ← i + 1
	od

	print newline

end
