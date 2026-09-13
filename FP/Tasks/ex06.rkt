#lang racket

(require racket/trace)

; map, filter, foldr, foldl, apply

(map (λ (x) (* x 2)) '(1 2 3 4))

(map (λ (a b) (+ (* a 2) b)) '(1 2 3) '(4 5 6))

(filter odd? '(1 2 3 4 5))

(foldl cons '() '(1 2 3 4 5)) ; -> '(5 4 3 2 1)

(foldr cons '() '(1 2 3 4 5)) ; -> '(1 2 3 4 5)

(apply + 10 '(1 2 3 4))

(define (remove-last xs)
  (reverse (rest (reverse xs))))

(rest '(1 2 3 4))
(remove-last '(1 2 3 4))

(define (ordered? xs pred)
  (or (empty? xs)
      (empty? (rest xs))
      (and (pred (first xs) (second xs))
           (ordered? (rest xs) pred))))

(ordered? '(1 2 3 4) <)
(ordered? '(1 3 2 4) <)

(sort '(6 3 2 1 3) <)
(sort '(6 3 2 1 3) >)

(define (longest-prefix xs)
  (cond [(empty? xs) '()]
        [(empty? (rest xs)) xs]
        [(< (first xs) (second xs)) (cons (first xs)
                                          (longest-prefix (rest xs)))]
        [else (list (first xs))]))
(longest-prefix '(1 2 3 4 1))

(define (max-ordered-sublist xs)
  (define (helper xs res)
    (define new-sublist (longest-prefix xs))
    (cond [(empty? xs) res]
          [(> (length new-sublist) (length res))
             (helper (drop xs (length new-sublist))
                     new-sublist)]
          [else (helper (drop xs (length new-sublist))
                        res)]))
  (trace helper)
  (helper xs '()))
(max-ordered-sublist '(1 2 1 2 3 4))
(max-ordered-sublist '(1 2 3 4 1 2 1))

(define (flatten xss)
  (cond [(empty? xss) '()]
        [(list? (first xss)) (append (flatten (first xss))
                                     (flatten (rest xss)))]
        [else (cons (first xss) (flatten (rest xss)))]))

(flatten '((1 2 3) (4 5 6) () ((7 8) (9 10 (11 (12)))))) ; -> '(1 2 3 4 5 6 7 8 9 10 11 12)

; '((1 . 10) (2 . 11))

(define (assoc key a-list)
  (cond [(empty? a-list) #f]
        [(equal? key (caar a-list)) (cdar a-list)]
        [else (assoc key (rest a-list))]))
(assoc 2 '((1 . 2) (2 . b)))
(assoc 5 '((1 . 2) (2 . b)))


(define (replace lst dict)
  (map (λ (key) (assoc key dict)) lst))

(replace '(1 2 3 4 5) '((1 . a) (2 . b) (3 . c) (4 . d)))

(define (replace-2 lst dict)
  (define (find key)
    (define value (assoc key dict))
    (if value value key))
  (map find lst))

(replace-2 '(1 2 3 4 5) '((1 . a) (2 . b) (3 . c) (4 . d)))

(define (deep-delete xs)
  (define (helper k xs)
    (cond [(empty? xs) '()]
          [(list? (first xs)) (cons (helper (+ k 1) (first xs))
                                    (helper k (rest xs)))]
          [(<= k (first xs)) (cons (first xs)
                                   (helper k (rest xs)))]
          [else (helper k (rest xs))]))
  (helper 1 xs))
(deep-delete '(1 (2 (2 4) 1) 0 (3 (1)))) ; -> (1 (2 (4)) (3 ())))


(define (diagonal mat)
  (if (empty? mat)
      '()
      (cons (caar mat)
            (diagonal (rest (map rest mat))))))

(define matrix '(( 1  2  3  4)
                 ( 5  6  7  8)
                 ( 9 10 11 12)
                 (13 14 15 16)))
(diagonal matrix) ; -> (1 6 11 16)

(range 1 11)


(define (tabulate f)
  (λ (a b) (map (λ (x) (cons x (f x)))
                (range a (+ b 1)))))
((tabulate sqr) 1 5) ; -> '((1 . 1) (2 . 4) (3 . 9) (4 . 16) (5 . 25))