program linearsearch
begin
	var n, i, target : int
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

	read(target)

	i  ← 0
	do i < n  → 
		if a[i] = target → 
			ans ← i
			i ← n
		fi
		i ← i + 1
	od

	print ans

end
