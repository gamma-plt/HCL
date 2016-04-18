program example3
begin
	var x : int;
	var y : int;

	x, y ← 23524, 7654;
	do x < y → y ← y - x # Test comment
	 □ y < x → x ← x - y
	od

	# More comments
	var q : int;
	var r : int;
	var D : int;

	q, r ← 0, 8105;
	D ← 3564;

	do r ≥ D →
		r ← r - D;
		q ← q + 1
	od

	var i : int;
	var j : int;
	var N : int;
	var X : int;
	var present : boolean;

	N ← 10;
	X ← 5;

	var A : array[0 .. 10] of int;

	i, j ← 0, N + 1;
	do i < j - 1 →
		var m : int;
		m ← (i + j) / 2;
		if A[m] < X → i ← m
		 □ A[m] = X → i, j ← m, n
		 □ A[m] > X → j ← m
		fi
	od;
	present ← (i = j);

	print present
end
