#lang racket

(define a 2)
(define b 2)

(= 2 2.0)
(= a b)

(eq? a b)
(equal? a b)

(cons 1 2)
(cons 1 (cons 2 (cons 3 4)))

'()
(cons 1 (cons (cons 2.1 2.2) (cons 3 '())))
(cons 1 (cons (cons 2.1 '()) (cons 3 '())))

(pair? 2)
(pair? '())
(pair? '(1 . 2))

(equal? (list 1 (cons 2 5) 3) '(1 (2 . 5) 3))
(eqv? 2 2)
(eqv? (list 1 (cons 2 5) 3) '(1 (2 . 5) 3))
(eqv? '() (list))
(list? 2)
(list? '(1 . 2))
(list? '(1 2))

(car '(1 . 2))
(cdr '(1 . 2))

(caddr '(1 2 3))

(car '(1 2))
(cdr '(1 2))
(cdr '(1 2 3))
(car '(1))
(cdr '(1))

(first '(1 2 3))
(second '(1 2 3))
(rest '(1 2 3))

(empty? '())
(empty? '(1 2))

(define (size lst)
  (if (empty? lst)
      0
      (+ 1 (size (rest lst)))))
(size '(1 2 3 4))

(size '((1) (2 3 4 #t) (λ (x) (* x 2))))

(third '((1) (2 3 4 #t) (λ (x) (* x 2))))
(third (list '(1) '(2 3 4 #t) (λ (x) (* x 2))))

;((third '((1) (2 3 4 #t) (λ (x) (* x 2)))) 5)
((third (list '(1) '(2 3 4 #t) (λ (x) (* x 2)))) 5)


(define (in-list x lst)
  (and (not (empty? lst))
       (or (equal? x (first lst))
           (in-list x (rest lst)))))
(in-list 4 '(1 2 3 4))
(in-list 5 '(1 2 3 4))

(define x 10)
'(x)
(list x)

(define (insert x pos lst)
  (if (= pos 0)
      (cons x lst)
      (cons (first lst) (insert x (- pos 1) (rest lst)))))

(insert 11 3 '(1 2 3 4 5 6 7 8 9 10))
(insert 11 0 '(1 2 3 4 5 6 7 8 9 10))

(define (minimum lst)
  (if (empty? (rest lst))
      (first lst)
      (min (first lst) (minimum (rest lst)))))
(minimum '(4 3 12 2 3 4))

(count (λ (x) (= x 10)) '(10 10 1))

(define (remove-first x lst)
  (cond [(empty? lst) '()]
        [(equal? x (first lst)) (rest lst)]
        [else (cons (first lst) (remove-first x (rest lst)))]))
(remove-first 3 '(1 2 3 4 3 3 4))

(define (remove-all x lst)
  (cond [(empty? lst) '()]
        [(equal? x (first lst)) (remove-all x (rest lst))]
        [else (cons (first lst) (remove-all x (rest lst)))]))
(remove-all 3 '(1 2 3 4 3 3 4))

(define (append as bs)
  (if (empty? as)
      bs
      (cons (first as) (append (rest as) bs))))
(append '(1 2 3) '(4 5 6))
(append '(1 2 3) '(4))


(define (reverse-rec xs)
  (if (empty? xs)
      '()
      (append (reverse-rec (rest xs)) (list (first xs)))))
(reverse-rec '(1 2 3 4 5))


(define (reverse xs)
  (define (helper xs rev)
    (if (empty? xs)
        rev
        (helper (rest xs) (cons (first xs) rev))))
  (helper xs '()))
(reverse     '(1 2 3 4 5))


; drop, take
(take '(0 1 2 3 4) 3)
(drop '(0 1 2 3 4) 3)

(define (sublist-between start end xs)
  (take (drop xs start) (+ 1 (- end start))))

(sublist-between 2 5 '(0 1 2 3 4 5 6 7))

; count
(count even? '(0 1 2 3 4 5 6))

(define (count-occcurrences subxs xs)
  (count (λ (x) (equal? x subxs)) xs))

(count-occcurrences 2 '(1 2 3 4 2 2 3))
(count-occcurrences '(0 1) '((0 1) (2) (0 1) (5)))
