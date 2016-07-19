program summation
begin

   var n, sum, i : int
   var r,e,s,u,l,t,colon : char
   
   n, sum, i ← 0, 0, 0
   read(n)
   do i ≤ n →
      sum ← sum + i
      i ← i+1
   od
   
   r ← "R"
   e ← "e"
   s ← "s"
   u ← "u"
   l ← "l"
   t ← "t"
   colon ← ":"
   print r
   print e
   print s
   print u
   print l
   print t
   print colon
   print " "
   print sum
   print "\n"
end
