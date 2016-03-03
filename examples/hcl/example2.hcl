begin
	var m : int;
	x, m ← 0, N;
	do m ≠ x →
		if ¬f(x) → x ← x + 1
		 □ f(x)  → m ← x
		fi
	od
end
