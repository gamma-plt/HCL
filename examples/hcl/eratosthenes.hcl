program eratosthenes
begin
	var n, i, j : int
	n, i, j ← 30, 2, 0
	var A : array[2 .. 30] of boolean
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
