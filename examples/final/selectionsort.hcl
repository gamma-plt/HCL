program selectionsort
begin
	var n, i, j, target : int
	var low, upp, ans : int
	var a : array[0 .. 100] of int

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

	j ← 0
	do j < n - 1 →
		var imin : int

		i ← j + 1
		do i < n →
			if a[i] < a[imin] →
				imin ← i
			fi
			i ← i + 1
		od

		if imin ≠ j →
			temp ← a[j]
			a[j] ← a[imin]
			a[imin] ← temp
		fi

		j ← j + 1
	od

	i ← 0
	do i < n  → 
		print a[i] 
		print space
		i ← i + 1
	od

	print newline

end
