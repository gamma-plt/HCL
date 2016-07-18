program eratosthenes
begin
	var n, i, j : int
	n, i, j ← 0, 0, 0
	read(n)
	var A : array[2 .. 100] of boolean
	
	do i < n →
		A[i] ← true
		i ← i + 1
	od;

	i ← 2
	do i * i < n →
		if A[i] → 
			j ← i * i
			do j < n →
				A[j] ← false
				j ← j + i
			od
		fi
		i ← i + 1
	od

	i ← 2
	do i < n →
		if A[i] → print i fi
		i ← i + 1
	od;
end
