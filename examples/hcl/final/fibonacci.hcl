program fibonacci
begin
    var f0, f1, ft, n, i : int
    var newline : char
    newline ← "\n"

    read(n)
    print newline

    f0, f1, i, ft ← 0, 1, 0, 0
    

    do i < n →
        ft ← f0 + f1
        f0, f1 ← f1, ft
        i ← i + 1 

        print f0
        print newline
    od    
end
