program collatz
begin
	var n : int
	var newline, space : char
	newline ← "\n"
    space ← " "
    
	read(n)
	print newline

	do even(n) → 
		n ← n / 2
		print n 
		print space
	□ ¬even(n) ∧ n > 1 →
	 	n ← 3 * n + 1
	 	print n
	 	print space
	od

	print newline
end
