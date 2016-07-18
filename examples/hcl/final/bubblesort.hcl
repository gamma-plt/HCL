program bubblesort
begin
	var n, i, j, target : int
	var low, upp, ans : int
	var a : array[0 .. 20] of int

	read(n)
	low, upp, ans ← 0, 10, -1

	i  ← 0
	do i < n  → 
		a[i] ← rand(low, upp)
		i ← i + 1
	od

	i ← 0
	do i < n  → 
		print a[i] 
		i ← i + 1
	od

	var temp : int

	i  ← 0
	do i < n  → 
		j  ← 1
		do j < n - 1 →
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
		i ← i + 1
	od

end
