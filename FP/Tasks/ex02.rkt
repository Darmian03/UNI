#lang racket

(define (in-range? x a b)
  (and (<= a x) (<= x b)))

(in-range? 10 1 15)
(in-range? -10 1 15)

(= 0 (remainder 10 4))

(define (gcd a b)
  (if (= b 0)
      a
      (gcd b (remainder a b))))

(gcd 7 11)
(gcd 14 21)

(define (mymaxdivisor x)
  (define (helper d)
    (if (= 0 (remainder x d))
        d
        (helper (- d 1))))
  (helper (- x 1)))

(mymaxdivisor 225)


(= 1 (remainder 11 2))
(odd? 11)
(even? 11)

(define (sum-odds a b)
  (cond [(> a b)  0]
        [(odd? a) (+ a (sum-odds (+ a 1) b))]
        [else     (sum-odds (+ a 1) b)]))

(sum-odds 1 10)


(define (prime? n)
  (and (> n 1) (= 1 (mymaxdivisor n))))

(prime? 1)
(prime? 2)
(prime? 4)
(prime? 7)

; (reverse-number 1234) -> 4321
; 4321 = 4 * 10^3 + 3 * 10^2 + 2 * 10^1 + 1 * 10^0
; 4321 = (((0 * 10 + 4) * 10 + 3) * 10 + 2) * 10 + 1

(define (reverse-number n)
  (define (helper res k)
    (if (< k 10)
        (+ (* res 10) k)
        (helper (+ (* res 10) (remainder k 10))
                (quotient k 10))))
  (helper 0 n))

(reverse-number 1234)

; (reverse-number 1234) -> (helper 0 1234) -> (helper 4 123)
; -> (helper 43 12) -> (helper 432 1) -> (+ (* 432 10) 1)
; -> 4321

; (palindrome? 12321) -> #t

(define (palindrome? n)
  (= n (reverse-number n)))

(palindrome? 123321)
(palindrome? 12312)

(define (count-palindromes a b)
  (cond [(> a b)         0]
        [(palindrome? a) (+ 1 (count-palindromes (+ a 1) b))]
        [else            (count-palindromes (+ a 1) b)]))

(count-palindromes 0 20)

(define (count-divisors n)
  (define (helper count d)
    (cond [(> d n)               count]
          [(= 0 (remainder n d)) (helper (+ 1 count) (+ d 1))]
          [else                  (helper count (+ d 1))]))
  (helper 0 1))

(count-divisors 14)
