program randomarray
begin
	var n, i : int
	var a : array[0 .. 20] of int

	read(n)

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
end
