program fibonacci
begin
    var f0, f1, ft, n, i : int
    read(n)
    f0,f1,i ← 0,1,0
    do i < n →
       ft ← f0+f1
       f0,f1 ← f1,ft
       i ← i+1  
    od
    print f0
    print f1
end
