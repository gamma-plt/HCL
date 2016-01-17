begin
	var n, c, N : int;
	n, c ← 0, 0;

	N ← 37

	var X : array of int;

	X[0] ← 1;
	...
	X[36] ← 4;

	do n ≠ N ∧ c ≠ 2 → 
		if X[n] = 0 → c ← c + 1
	     ▯ X[n] ≠ 0 → skip
	    fi;
	    n ← n + 1
	od;

	if c < 2 → r ← ∞
	 ▯ c = 2 → 
	 	begin
	 		var s, t, r : int;
	 		s ← 0;
	 		do X[s] ≠ 0 → s ← s + 1 od;
	 		t ← s + 1;
	 		do X[t] ≠ 0 → t ← t + 1 od;
	 		n ← t + 1;
			r ← n - s;
			do n ≠ N →
				if X[n] ≠ 0 → skip
				 ▯ X[n] = 0 → s, t ← t, n
				fi;
				r ← r min (n + 1 - s);
				n ← n + 1
			od
	 	end
	fi
end