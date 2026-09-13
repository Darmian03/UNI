#lang racket

#|
Define a function that accepts an infinite list of numbers [x1, x2 .. ]
and returns a function that for every
`x` and `y` calculates the expression (x - x1) (x - x2) ..  (x - xy).
In Racket we don't have infinite lists, so limit the lists to `100`.

Test cases:
If g is myPoly [2.7, 3.0 ..]
    then g 2.2 3 -> -0.4399999999999998
If g is myPoly [2, 3 ..]
    then g 2.2 3 -> 0.2880000000000002
|#

(define (my-poly xs)
  (λ (x y) (apply * (map (curry - x) (take xs y))))
  )

(= ((my-poly (range 2.7 101 0.3)) 2.2 3) -0.4399999999999998)
(= ((my-poly (range 2 101)) 2.2 3) 0.2880000000000002)
