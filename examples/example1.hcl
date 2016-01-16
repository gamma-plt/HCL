|
	var n, c : int;
	n, c := 0, 0;

	do n <> N /\ c <> 2 ->
		if 
			X[n] = 0 -> c := c + 1
			:: X[n] <> 0 -> skip
		fi
	od;

	if
		c < 2 -> r := INFTY
		:: c = 2 ->
			|
				var s. t : int;
				s := 0;
				do X[s] <> 0 -> s := s + 1 od;
				t := s + 1;
				do X[t] <> 0 -> t := t + 1 od;
				n := t + 1;
				r := n - s;
				do 
					n <> N -> 
						if 
							X[n] <> 0 -> skip
							:: X[n] = 0 -> s, t := t, n
						fi;
						r := r min (n + 1 - s);
						n := n + 1
				od
			|
	fi
|

fun max(a, b : int) |
	var c : int;
	if a < b  -> c := b;
	[] b <= a -> c := a
	fi;
	free c
|

|
	var x, y, N : int;
	x, y := 0, 0;

	do x <> 0 -> x := x - 1
	[] y <> N -> x, y := x + 1, y + 1
	od
|
