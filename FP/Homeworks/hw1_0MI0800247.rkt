#lang racket/base


(define (bouncing-ball height bounce window)
  (if (<= height window) -1
      (+ 2 (bouncing-ball (* height bounce) bounce window))))

(bouncing-ball 3 0.66 1.5)
(bouncing-ball 30 0.66 1.5)
(bouncing-ball 10 0.6 10)
(bouncing-ball 2 0.5 1.0)



(define (num-apples lifespan year)
  (define (helper span year sum apples)
    (if (> year span) sum
      (helper span (+ year 1) (+ sum (* 3 apples)) (floor (/ (* 4 apples) 5)))))
  (if (or (< year 1) (< lifespan 1)) -1
      (helper (min year lifespan) 1 0 300)))

(num-apples 2 1)
(num-apples 4 8)
(num-apples 74 10)
(num-apples 1 15)
(num-apples 52 77)