{-
Define a function that accepts a one-argument function
and a list of numbers [y1, y2 .. yn]
and returns a function that for every `x` calculates the
expression f(y1 x) + 2f(y2 x) + .. + nf(yn x).
Notes:
- Solve the task with one line of code!
- Solve the task with typeclasses!

Test cases:
    If g is myPolynomial (\x -> x - 2) [1, 4, 7, 8, 5, 2], then g 5 -> 453
    If g is myPolynomial (\x -> x + 10) [3.62, 6.12, 9.45, 8.02, 5, 2], then g (-5) -> -356.45
-}

main :: IO()
main = do
    print $ (myPolynomial (\x -> x - 2) [1, 4, 7, 8, 5, 2]) 5 == 453
    print $ (myPolynomial (\x -> x + 10) [3.62, 6.12, 9.45, 8.02, 5, 2]) (-5) == -356.45

myPolynomial :: (Num a, Enum a) => (a -> a) -> [a] -> (a -> a)
myPolynomial f ys = (\ x -> sum $ zipWith (\ yi pos -> pos * f (yi * x)) ys [1 ..])
