program example2
begin
	var m : int;
	var x : int;
	x, m ← 0, 34543;
	do m ≠ x →
		if ¬f(x) → x ← x + 1
		 □ f(x)  → m ← x
		fi
	od
end
