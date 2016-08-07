;; program Eratosthenes
((var (n i j) int)
(set (n i j) (0 0 0)))
(read n)

(var a (array 100 bool))

(do (< i n)
	((set (idx A i) true) 
		(inc i)))

(set i 2)
(do (< (* i i) n)
	((if (idx A i) 
		((set j (* i i))
			(do (< j n)
				((set (idx A j) false) (inc j)))
	)) (inc i)))

(set i 2)
(do (< i n)
	((if (idx A i) ((print i))) (inc i)))

;; program collatz
(var n int)
(var (newline space) char)
(set (newline space) ("\n" " "))
(read n)
(print newline)

(do (even n) 
		((set n (/ n 2)) (print n) (print space))
	(and (not (even n)) (> n 1)) 
		((set n (* 3 (+ n 1))) (print n) (print space)))

(print newline)