#lang racket

(require racket/trace)

(define % remainder)
(define // quotient)

(define (ends-with? a b)
  (or (and (< a 10)
           (= a (% b 10)))
      (and (= (% a 10) (% b 10))
           (ends-with? (// a 10) (// b 10)))))

(trace ends-with?)

(ends-with? 12 312)
(ends-with? 121 312)
(ends-with? 1 131)
(ends-with? 1234 31234)

(define (substr? a b)
  (or (ends-with? a b)
      (and (<= a b)
           (substr? a (// b 10)))))

(substr? 12 1122)
(substr? 123 1122)
(substr? 1 1122)
(substr? 1234 11221234)
(substr? 1234 11234212634)

(define (my-identity x) x)

; h(x) = f(x) . g(x) = f(g(x))

;(define (my-compose f g)
;  (define (h x)
;    (f (g x)))
;  h)

(define (my-compose f g)
  (λ (x) (f (g x))))

((my-compose (λ (x) (+ x 2)) (λ (x) (* x 5))) 5)
(define f1 (my-compose (λ (x) (+ x 2)) (λ (x) (* x 5))))
(f1 5)

;(define (my-negate p?)
;  (my-compose not p?))

(define (my-negate p?)
  (λ (x) (not (p? x))))

((my-negate odd?) 15)
((my-negate odd?) 16)

(define (f3 a b c)
  (* a (+ b c)))

(f3 1 2 3)

;(f3 1)

(define (my-curry f x)
  (λ (b c) (f x b c)))

((my-curry f3 1) 2 3)

f3
(((curry f3) 1) 2 3)
(((curry f3) 1 2) 3)
((((curry f3) 1) 2) 3)

(define f3_1 ((curry f3) 1))

((f3_1 2) 3)

(curry f3 1 2)
(λ (c) (f3 1 2 c))

; λ === Ctrl + \


(define (difference F a b)
  (- (F b) (F a)))

(difference (λ (x) (* x 2)) 3 7)


(define f4 (λ (x) (* x 2)))

(f4 10)

(define (f5) (* 10 2))


(define (derive f eps)
  (λ (x) (/ (- (f (+ x eps)) (f x)) eps)))

((derive (λ (x) (* 2 x x)) 1e-3) 2)


(define (switchsum f g n)
  (define (helper i prev sum)
    (if (= i n)
        (+ sum prev)
        (helper (+ i 1)
                (if (even? i)
                    (f prev)
                    (g prev))
                (+ sum prev))))
  (λ (x) (helper 1 (f x) 0)))

((switchsum (λ (x) (+ x 1)) (λ (x) (* x 2)) 1) 2)
((switchsum (curry + 1)     (curry * 2)     2) 2)
((switchsum (λ (x) (+ x 1)) (λ (x) (* x 2)) 3) 2)
((switchsum (λ (x) (+ x 1)) (λ (x) (* x 2)) 4) 2)