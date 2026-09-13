#lang racket

(require racket/trace)

(define % remainder)
(define // quotient)

(% 10 3)
(// 10 3)

(define (prime? n)
  (define (helper d)
    (cond [(= n d) #t]
          [(= 0 (remainder n d)) #f]
          [else (helper (+ d 1))]))      
  (and (> n 1) (helper 2)))

(define (sum-prime-divisors n)
  (define (helper d sum)
    (cond [(> d n) sum]
          [(and (= 0 (% n d)) (prime? d))
              (helper (+ d 1) (+ sum d))]
          [else (helper (+ d 1) sum)]))
  ;(trace helper)
  (helper 2 0))

(trace sum-prime-divisors)

(sum-prime-divisors (* 7 13))


(define (pow x n)
  (if (= n 0)
      1
      (* x (pow x (- n 1)))))

;(trace pow)
(pow 2 10)
(pow 3 5)

(define (count-оccurences d n)
  (cond [(< n 10) (if (= n d) 1 0)]
        [(= d (% n 10)) (+ 1 (count-оccurences d (// n 10)))]
        [else (count-оccurences d (// n 10))]))

;(trace count-оccurences)
(count-оccurences 2 1232221)

(define (ascending? n)
  (or (< n 10)
      (and (<= (% (// n 10) 10) (% n 10))
           (ascending? (// n 10)))))

(ascending? 1233345)
(ascending? 1243345)

(define (filtered-sum p? a b)
  (cond [(> a b) 0]
        [(p? a) (+ a (filtered-sum p? (+ a 1) b))]
        [else (filtered-sum p? (+ a 1) b)]))

(filtered-sum even? 1 10)

(define (perfect-number? n)
  (define (divisor-n? d)
    (= 0 (% n d)))
  (= n (filtered-sum divisor-n? 1 (- n 1))))

(perfect-number? 6)
(perfect-number? 27)
(perfect-number? 28)
(perfect-number? 8128)


; Ctrl + \ === lambda === λ

(define (perfect-number-2? n)
  (= n (filtered-sum (λ (d) (= 0 (% n d))) 1 (- n 1))))

(perfect-number-2? 6)
(perfect-number-2? 27)
(perfect-number-2? 28)
(perfect-number-2? 8128)


;(define (f1 a)
;  (define (helper b)
;    (* a b b))
;  helper)

(define (f1 a)
  (λ (b) (* a b b)))

((f1 10) 2)
((f1 10) 3)

(define f1-10 (f1 10))
(f1-10 2)
(f1-10 3)

(define f2-1 (λ (a b) (* a b b)))
(define (f2-2 a b)
  (* a b b))
(f2-1 1 2)
(f2-2 1 2)

(define (f3) (λ (x) (* x x x)))
((f3) 10)


(define (calc-sum x n)
  (define (helper prev i sum)
    (if (> i n)
        (+ sum prev)
        (helper (* x prev) (+ i 1) (+ sum prev))))
  (helper 1 1 0))

(calc-sum 2 0)
(calc-sum 2 1)
(calc-sum 2 2)