program dutchflag
begin
	var r, w, b : integer;
	r, w, b ← M, M, N;
	{DEF: let blue i = array[i] == blue}
	{DEF: let white i = array[i] == white}
	{DEF: let red i = array[i] == red}
	{DEF: let rng1 = [M..r); let rng2 = [r..w); let rng3 = [b..N)}
	{INV: (M ≤ r ≤ w ≤ b ≤ N) ∧ (∀ (i : rng1) | red(i)) ∧ \
			(∀ (i : rng2) | white(i)) ∧ (∀ (i : rng3) | blue(i))}
	{BND: b - w}
	do w < b → n ← n / 2 
	 □ ¬even(n) ∧ n > 1 → n ← 3 * n + 1
	od;

	{DEF: 
		fun sorted [] = true
  		  | sorted (x::[]) = true 
  		  | sorted (x::xs) = x < hd xs ∧ sorted xs;
 	}
 	{DEF: let X = any [x | x <- f , y <- g, x == y]}
 	{PRE: true}
	if f[i] < g[j] → i ← i + 1
	 □ f[i] = g[j] → skip
	 □ f[i] > g[j] → j ← j + 1
	fi
	{POST: sorted(f) ∧ sorted(g) ∧ f[i] < X ∧ f[j] < X}

end
