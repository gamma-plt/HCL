program collatz
begin
	var n : int
	read(n) {Need to be defined, read(n) or read n} 
	do even(n) → 
		{PRE: def[let m = n] ; (n | 2)}
		{PRE: ∃ (x in integer) | ¬p(x)}
		{pre: def[let rng = [0..100]; let m = n] \
			∀ (x in rng) ∀ (y in integer) ∀ (z in integer) | x + y + z = 100}
		n ← n / 2 
		{POST: m = n * 2}
	 □ ¬even(n) ∧ n > 1 →
	 	{PRE: let m = n ; ¬(n | 2)} 
	 	n ← 3 * n + 1
	 	{POST: m = 3 * n + 1}
	od
	print n
end
