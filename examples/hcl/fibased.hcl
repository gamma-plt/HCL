program fibased
begin
	var n, m, max, min : integer;
	var a0, a1, f0, f1 : integer;
	var prod : integer;

	max, min ← max(n, m), min(n, m);
	f0, f1, a0, a1, product ← 1, 2, max, max + max, 0;
	
	do f0 + f1 ≤ min → 
		a0, a1 ← a1, a0 + a1;
		f0, f1 ← f1, f1 + f0
	od;

	do min > 0 → 
		if fi ≤ min → 
			product, min ← product + a1, min - f1
	 	 □ fi > min → 
	 	 	f0, f1, a0, a1 ← f1 - f0, f0, a1 - a0, a0;
		fi
	od;
end