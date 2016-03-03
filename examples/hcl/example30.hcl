x, y ← X, Y;
do x < y → y ← y - x #Test comment
 □ y < x → x ← x - y
od
#More comments
q, r ← 0, X;
do r ≥ D →
	r ← r - D;
	q ← q + 1
od

i, j ← 0, N + 1;
do i < j - 1 →
	m ← (i + j) div 2;
	if A[m] < X → i ← m
	 □ A[m] = X → i, j ← m, n
	 □ A[m] > X → j ← m
	fi
od;
present ← (i = j) 
