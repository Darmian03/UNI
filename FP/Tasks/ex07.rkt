#lang racket

(define (shuffle-merge xs ys)
  (cond [(empty? xs) ys]
        [(empty? ys) xs]
        [else (cons (first xs)
                    (cons (first ys)
                          (shuffle-merge (rest xs) (rest ys))))]))

(shuffle-merge '(1) '())               ; → '(1)
(shuffle-merge '(3 4 5) '(2))          ; → '(3 2 4 5)
(shuffle-merge '(3 4 5) '(9 2))        ; → '(3 9 4 2 5)
(shuffle-merge '(3 2 8) '(5 6 1 9 11)) ; → '(3 5 2 6 8 1 9 11)


(define (get-missing-length xss)
  (define (find xss)
    (define (helper xss)
      (if (= (add1 (first xss)) (second xss))
          (helper (rest xss))
          (add1 (first xss))))
    (helper (sort (map length xss) <)))
  (if (or (empty? xss)
          (member '() xss))
      (error "Empty list!")
      (find xss)))

(get-missing-length '((1 2) (4 5 1 1) (1) (5 6 7 8 9))) ; → 3

(get-missing-length '(("a", "a", "a") ("a", "a") ("a", "a", "a", "a") ("a") ("a", "a", "a", "a", "a", "a"))) ; → 5


(define (where list-elements list-predicates)
  (filter (λ (x) (foldl (λ (p? res) (and res
                                         (p? x)))
                        #t
                        list-predicates))
          list-elements))

(where '(3 4 5 6 7 8 9 10) (list even? (lambda (x) (> x 5)))) ; → (6 8 10) (списък от всички елементи на дадения, които са четни числа, по-големи от 5)
(where '(3 4 5 7) (list even? (lambda (x) (> x 5)))) ; → () (в списъка няма четни числа, по-големи от 5)


(define (num-bigger-elements lst)
  (map (λ (x) (list x
                    (length (filter (curry < x)
                                    lst))))
       lst))

(num-bigger-elements '(5 6 3 4)) ; → '((5 1) (6 0) (3 3) (4 2)) 
(num-bigger-elements '(1 1 1))   ; → '((1 0) (1 0) (1 0))

(cdar '((1 . 2) (2 . 3) (3 . 4)))
(cdr (car '((1 . 2) (2 . 3) (3 . 4))))


(define (contains-points? lst f)
  (foldl (λ (p res) (and res
                         (equal? (f (car p))
                                 (cdr p))))
         #t
         lst))

(contains-points? '((1 . 2) (2 . 3) (3 . 4)) add1) ; → #t
(contains-points? '((1 . 2) (2 . 4) (3 . 4)) add1) ; → #f
(contains-points? '((1 . "11") (2 . "21") (3 . "31")) (λ (x) (string-append (number->string x) "1"))) ; → #t