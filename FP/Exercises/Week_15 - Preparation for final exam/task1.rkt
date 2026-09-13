#lang racket

(require racket/trace)

#|
Define TWO functions that take two numbers and return the sum of the numbers in
the interval [a, b] whose digits are ordered in a descending order.
The first function should implement a recursive process. The second function should use lists.
Examples:
- 222 IS a number whose digits are ordered in a descending order since: 2 >= 2 >= 2
- 201 IS NOT a number whose digits are ordered in a descending order since: 2 >= 0 < 1
|#

(define (descending-digits? n)
  (or
   (< n 10)
   (and
    (<=
     (remainder n 10)
     (remainder (quotient n 10) 10)
     )
    (descending-digits? (quotient n 10))
   )
   )
  )

;(trace descending-digits?)

(define (sum-numbers-xs-rec x y)
  (cond
    [(> x y) 0]
    [(descending-digits? x) (+ x (sum-numbers-xs-rec (add1 x) y))]
    [else (sum-numbers-xs-rec (add1 x) y)]
    )
  )

(define (sum-numbers-xs-lin-rec x y)
  (define (helper current-x res)
    (cond
      [(> current-x y) res]
      [(descending-digits? current-x) (helper (add1 current-x) (+ res current-x))]
      [else (helper (add1 current-x) res)]
      )
    )
  (helper x 0)
  )

(define (sum-numbers-xs x y)
  ;(foldl (λ (n acc) (if (descending-digits? n) (+ acc n) acc)) 0 (range x (add1 y)))
  (apply + (filter descending-digits? (range x (add1 y))))
  )

(= (sum-numbers-xs 1 9) 45)
(= (sum-numbers-xs 199 203) 200)
(= (sum-numbers-xs 219 225) 663)

(= (sum-numbers-xs-rec 1 9) 45)
(= (sum-numbers-xs-rec 199 203) 200)
(= (sum-numbers-xs-rec 219 225) 663)

(= (sum-numbers-xs-lin-rec 1 9) 45)
(= (sum-numbers-xs-lin-rec 199 203) 200)
(= (sum-numbers-xs-lin-rec 219 225) 663)
