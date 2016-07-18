program summation
begin
   var n, sum, i : int
   n, sum, i ← 0, 0, 0
   read(n)
   do i ≤ n →
      sum ← sum + i
      i ← i+1
   od
   print sum
end
