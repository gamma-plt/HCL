program mergesort
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

	print newline

	var curr_size, left_start, mid : int;
	var bound, dummy1, dummy2, right_end : int;
	dummy1 ← n - 1

	curr_size ← 1;
	do curr_size ≤ (n - 1) →

		left_start ← 0
		do left_start < (n - 1) →
			
			bound ← left_start + curr_size - 1
			mid ← min(bound, dummy1)
			dummy2 ← left_start + 2 * curr_size - 1
			right_end ← min(dummy2, dummy1);

			var n1, n2, k : int

			n1 ← mid - left_start + 1
			n2 ← right_end - mid

			var left, right : array[0 .. 20] of int

			i ← 0
			do i < n1 →
				left[i] ← a[left_start + i]
				i ← i + 1
			od

			j ← 0
			do j < n2 →
				right[j] ← a[mid + 1 + j]
				j ← j + 1 
			od

			i, j, k ← 0, 0, left_start

			do i < n1 ∧ j < n2 →
				if left[i] ≤ right[j] →
					a[k] ← left[i]
					i ← i + 1
				□ left[i] > right[j] →
					a[k] ← right[j]
					j ← j + 1
				fi
				k ← k + 1
			od

			do i < n1 →
				a[k] ← left[i]
				i ← i + 1
				k ← k + 1
			od

			do j < n2 →
				a[k] ← right[j]
				j ← j + 1
				k ← k + 1
			od

			left_start ← left_start + 2 * curr_size

		od

		curr_size ← 2 * curr_size
	od


	i ← 0
	do i < n  → 
		print a[i] 
		print space
		i ← i + 1
	od

	print newline

end
