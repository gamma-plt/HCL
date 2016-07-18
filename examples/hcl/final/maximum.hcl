program maximum
begin
	var n, i, max, curr : int
	var a : array[0 .. 20] of int

	read(n)

	i, max, curr ← 0, -∞, 0

	do i < n  → 
		read(curr)
		a[i] ← curr
		i ← i + 1
	od

	i ← 0
	do i < n  → 
		max ← max(max, a[i]) 
		i ← i + 1
	od

	print max
end
