do even(n) → n ← n div 2
 ▯ ¬even(n) ∧ n > 1 → n ← 3 * n + 1
od

if b1 → s1
 ▯ b2 → s2
 ▯ b3 → s3
fi


{
	var m : int;
	x, m ← 0, N;
	do m ≠ x →
		if ¬f(x) → x ← x + 1
		 ▯ f(x)  → m ← x
		fi
	od
}