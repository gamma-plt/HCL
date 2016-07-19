program randomarray
begin
	var n, i : int
	var low, upp : int
	var a : array[0 .. 20] of int
	var newline, space : char
	newline ← "\n"
    space ← " "

	read(n)

	i ← 0
	low, upp ← 0, 10

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
end
