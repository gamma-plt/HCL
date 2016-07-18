program collatz
begin
	var n : int
	read(n)
	do even(n) → 
		n ← n / 2
		print n 
	□ ¬even(n) ∧ n > 1 →
	 	n ← 3 * n + 1
	 	print n
	od
end
