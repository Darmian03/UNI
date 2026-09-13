#lang racket

*

3

(+ 5 (* 2 7 2))

(define A 2)

(* 2 A)

(define (f1 a b c)
  (+ a b c))

(define (B)
  5)


(define (average x y)
  (/ (+ x y) 2))

(define (sqr x)
  (* x x))

(define (zad5 x y)
  (average (sqr x) (sqr y)))

; fact(0) = 1
; fact(n) = n * fact(n-1)

(define (fact n)
  (if (= n 0)
      1
      (* n (fact (- n 1)))))

(fact 4)

; (fact 3) -> (* 3 (fact 2)) -> (* 3 (* 2 (fact 1))) -> (* 3 (* 2 (* 1 (fact 0))))
; -> (* 3 (* 2 (* 1 1))) -> (* 3 (* 2 1)) -> (* 3 2) -> 6


(define (fact-iter n)
  (define (helper k res)
    (if (= k 0)
        res
        (helper (- k 1) (* res k))))
  (helper n 1))

(fact-iter 4)

; (fact-iter 3) -> (helper 3 1) -> (helper 2 3) -> (helper 1 6) -> (helper 0 6)
; -> 6

; 0 1 2 3 4 5  6 ...
; 1 1 2 3 5 8 13 ...

; fib(0) = 1
; fib(1) = 1
; fib(n) = fib(n-2) + fib(n-1), когато n>1

(define (fib n)
  (if (<= n 1)
      1
      (+ (fib (- n 2)) (fib (- n 1)))))

(fib 5)
(fib 6)
;(fib 50)

(define (fib-iter n)
  (define (helper i prev cur)
    (if (= i n)
        cur
        (helper (+ i 1) cur (+ prev cur))))
  (helper 0 0 1))

(fib-iter 5)
(fib-iter 6)
(fib-iter 500)