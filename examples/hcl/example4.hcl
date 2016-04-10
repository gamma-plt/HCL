program example4
begin
	var n, c, i, N : int
	n, c ← 0, 0

	N ← 37

	var X : array[0 .. 34] of int
	i ← 0
	
	do i ≠ N → X[i] ← i + 1 
	   i ← i + 1 
	od

	do n ≠ N ∧ c ≠ 2 → 
		if X[n] = 0 → c ← c + 1 g ← a
	     □ X[n] ≠ 0 → skip
	    fi
	    n ← n + 1
	od;

	if c < 2 → r ← ∞
	 □ c = 2 → 
	 		var s, t, r : int
	 		s ← 0
	 		do X[s] ≠ 0 → s ← s + 1 od
	 		t ← s + 1
	 		do X[t] ≠ 0 → t ← t + 1 od
	 		n ← t + 1
			r ← n - s
			do n ≠ N →
				if X[n] ≠ 0 → skip
				□ X[n] = 0 → s, t ← t, n
				fi
				r ← min(r, (n + 1 - s))
				n ← n + 1
			od
	fi
end
