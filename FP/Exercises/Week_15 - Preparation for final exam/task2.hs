{-
Define a function that accepts an infinite list of numbers [x1, x2 .. ]
and returns a function that for every `x` and `y` calculates the expression (x - x1) (x - x2) ..  (x - xy).
In Racket we don't have infinite lists, so limit the lists to `100`.

Test cases:
If g is myPoly [2.7, 3.0 ..]
    then g 2.2 3 -> -0.4399999999999998
If g is myPoly [2, 3 ..]
    then g 2.2 3 -> 0.2880000000000002
-}

main :: IO()
main = do
    print $ (myPoly [2.7, 3.0 ..]) 2.2 3 == -0.4399999999999998
    print $ (myPoly [2, 3 ..]) 2.2 3 == 0.2880000000000002

myPoly :: (Num a) => [a] -> (a -> Int -> a)
myPoly xs = (\ x y -> product $ map (x-) $ take y xs)
