main :: IO()
main = do
  print 10
  print (f1 10)
  print (f2 10)
  print (f3 1 2 3)
  print ((f3 1) 2 3)
  print (((f3 1) 2) 3)
  print ((+ 5) 10)
  print (((+ 5) . (* 2)) 10)
  print (map (* 2) [1..10])
  print (map (\ x -> x * 2) [1..10])
  print (zip [1,2,3] [5,7,9])
  print (zip [1,2,3,4,5] [5,7,9])
  print (map (\ (a, b) -> a + b) (zip [1,2,3] [5,7,9]))
  print [n | (i, n) <- zip [0..] [1..10], even i]
  print (f4 2 3)
  print (primesInRange 1 97)
  print (foldl (*) 1 [1..10])
  print (product [1..10])
  print (foldl1 (*) [1..10])
  print (foldr1 (*) [1..10])
  print (prodSumDiv [20..30] 12)
  print (insert 3 [1,2,4,5])
  print (merge [1,3,5] [2,4,6,8])
  print (insertionSort [4,3,2,5,6,1])
  print (maximum [3,4,2,1,5,0])
  print (maximum [(1, 2), (2, 5), (3, 10), (4, -1)])
  print (maximum [(1, 2), (2, 5), (3, 10), (3, 11), (3, 9)])
  print (fn 0.5)
  print (fn (-2))
  where fn = maximize [(\x -> x*x*x),(\x -> x+1)]


f1 :: Int -> Int
f1 x = 2 * x

f2 :: Int -> Int
f2 = \ x -> 2 * x

--f3 :: (Int -> (Int -> (Int -> Int)))
--f3 a b c = a * b + c

f3 :: Int -> (Int -> Int -> Int)
f3 a = \ b c -> a * b + c

f4 :: Int -> Int -> Int
f4 = f3 4
--f4 b c = f3 4 b c

isPrime :: Integer -> Bool
isPrime n = [d | d <- [1..n], mod n d == 0] == [1, n]

primesInRange :: Integer -> Integer -> [Integer]
primesInRange a b = [n | n <- [a..b], isPrime n]

prodSumDiv :: [Integer] -> Integer -> Integer
prodSumDiv ns k =
  product [n | n <- ns, mod (sumDivisors n) k == 0]
  where
    sumDivisors n = sum [d | d <- [1..n], mod n d == 0]

isSorted :: [Int] -> Bool
isSorted []  = True
isSorted [_] = True
isSorted (x1:x2:xs) =
  x1 <= x2 && isSorted (x2:xs)

insert :: Int -> [Int] -> [Int]
insert x [] = [x]
insert x zs@(x1:xs) =
  if x < x1 then x:zs
  else x1:insert x xs

merge :: [Int] -> [Int] -> [Int]
merge []         bs = bs
merge as         [] = as
merge pas@(a:as) pbs@(b:bs) =
  if a < b then a:merge as pbs
           else b:merge pas bs

insertionSort :: [Int] -> [Int]
insertionSort = foldr insert []

maximize :: (Ord a, Num a) => [(a -> a)] -> (a -> a)
maximize fs = \ x ->
  snd (maximum [(abs fx, fx) | fx <- [f x | f <- fs]])