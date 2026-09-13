#lang racket
(require srfi/13)
;нужна ми е за string-contains, иначе не мога да направя 2ра задача

;ЗАДАЧА 1
(define (cross-water-min-risk risks)
  (cond [(null? risks) 0]
        [(null? (cdr risks)) 0]
        [else (min (+ (first risks) (cross-water-min-risk (rest risks)))
                   (+ (second risks) (cross-water-min-risk (rest (rest risks)))))]))

(cross-water-min-risk '(10 15 20))
(cross-water-min-risk '(1 100 1 1 1 100 1 1 100 1))
(cross-water-min-risk '(458 896 809 929 430 241))
(cross-water-min-risk '(945 726 301 716 642 149))
(cross-water-min-risk '(192 31 533 573 772 31))
(cross-water-min-risk '(734 401 273 823 715 216 960 474 91 568))
(cross-water-min-risk '(793 413 20 210 963 733 992 500 660 43))


;ЗАДАЧА 2
(define (ith-manhattan cable1 cable2)
  (define (finder i l)
    (cond [(null? l) "Кабелите не се пресичат толкова пъти!"]
          [(= i 1) (first l)]
          [else (finder (- i 1) (rest l))]))
  (define (distance p)
    (+ (abs (car p)) (abs (last p))))
  (define cable-path1 (cable-path cable1))
  (define cable-path2 (cable-path cable2))
  (define list-of-intersections (sort (map distance (filter (λ (p) (member p cable-path1)) cable-path2)) <))
  (lambda (i) (finder i list-of-intersections)))

(define (cable-path cable)
  (define (move direction length point)
    (cond [(= length 0) '()]
          [(equal? direction "R") (cons (append (list (+ (car point) 1)) (list (last point)))
                                       (move direction (- length 1) (append (list (+ (car point) 1)) (list (last point)))))]
          [(equal? direction "U") (cons (append (list (car point)) (list (+ (last point) 1)))
                                       (move direction (- length 1) (append (list (car point)) (list (+ (last point) 1)))))]
          [(equal? direction "L") (cons (append (list (- (car point) 1)) (list (last point)))
                                       (move direction (- length 1) (append (list (- (car point) 1)) (list (last point)))))]
          [(equal? direction "D") (cons (append (list (car point)) (list (- (last point) 1)))
                                       (move direction (- length 1) (append (list (car point)) (list (- (last point) 1)))))]))
  (define (helper point steps)
    (cond [(equal? steps "") '()]
          [(not (number? (string-contains steps ","))) (move (substring steps 0 1) (string->number (substring steps 1 (string-length steps))) point)]
          [else (let ([newpoint (last (move (substring steps 0 1) (string->number (substring steps 1 (string-contains steps ","))) point))])
                  (append (move (substring steps 0 1) (string->number (substring steps 1 (string-contains steps ","))) point)
                          (helper newpoint (substring steps (+ 1 (string-contains steps ","))))))]))
  (helper '(0 0) cable))


((ith-manhattan "R8,U5,L5,D3" "U7,R6,D4,L4") 1)
((ith-manhattan "R75,D30,R83,U83,L12,D49,R71,U7,L72"
"U62,R66,U55,R34,D71,R55,D58,R83") 1) 
((ith-manhattan "R75,D30,R83,U83,L12,D49,R71,U7,L72"
"U62,R66,U55,R34,D71,R55,D58,R83") 2)
((ith-manhattan "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
"U98,R91,D20,R16,D67,R40,U7,R15,U6,R7") 1)
((ith-manhattan "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
"U98,R91,D20,R16,D67,R40,U7,R15,U6,R7") 3)
;((ith-manhattan ;//това се run-ва за 15сек (освен ако нямаш компютър на NASA)
;"R998,U367,R735,U926,R23,U457,R262,D473,L353,U242,L930,U895,R321,U683,L333,U623,L10005"
;"L998,U949,R912,D186,R359,D694,L878,U542,L446,D118,L927,U175,R434,U473,R147,D54,R896,U8890") 1)