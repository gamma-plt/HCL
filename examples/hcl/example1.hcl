program example1
begin
	var n : int;
	readint(n);
	do even(n) → n ← n / 2
	 □ ¬even(n) ∧ n > 1 → n ← 3 * n + 1
	od;
	print n
end
