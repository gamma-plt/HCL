program collatz
begin
	var n : int
	read(n) {Need to be defined, read(n) or read n} 
	do even(n) → 
		{PRE: let m = n ∧ (n | 2)} 
		n ← n / 2 
		{POST: m = n * 2}
	 □ ¬even(n) ∧ n > 1 →
	 	{PRE: let m = n ∧ ¬(n | 2)} 
	 	n ← 3 * n + 1
	 	{POST: m = 3 * n + 1}
	od
	print n
end
