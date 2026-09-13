import Data.Char
import Data.List

main :: IO()
main = do
  print ([1, 2, 3])
  print xs
  print ([] :: [Int])
  print (xs == [])
  print (xs == [1, 2, 3])
  print (null xs)
  print (head xs)
  print (tail xs)
  print (1:2:[])
  print (1:[2,3])
  print ([1,2] ++ [3,4])
  print v2
  print (fst v2)
  print (snd v2)
  print (v3)
  print (fst3 v3)
  print (fst3 (1, 2, 3))
  print (incrementAllBy [1..10] 2)
  print (incrementAllBy' [1..10] 2)
  print (ord 'a')
  print (chr 97)
  print (filterSmallerThan [1..10] 5)
  print (filterSmallerThan' [1..10] 5)
  print (filterSmallerThan'' [1..10] 5)
  print [(x + y, x, y) | x <- [1..4], y <- [5..7], x + y == 7]
  print [x | x <- [1..10], x > 3, x < 8]
  print [2 * x | x <- [1..10], x < 3 || x > 8, x < 9]
  print (toList 1234)
  print (check [1,2,3,4])
  print (check [1,3,2,4])
  print (isAscending 1234)
  print (isAscending 1324)
  print (digits "ab123c6")
  print (digitsSum "ab123c6")
  print (digitsSum' "ab123c6")
  print (capitalize "abABa34a")
  print (isCapitalized "ABCD1")
  print (isCapitalized "ABcD1")

xs :: [Int]
xs = [1, 2, 3]

v2 :: (Char, [Int])
v2 = ('a', [1,2,3])

v3 :: (Char, Int, [Double])
v3 = ('a', 3, [1..10])

fst3 :: (a, b, c) -> a
fst3 (x, _, _) = x

-- String === [Char]

incrementAllBy :: [Int] -> Int -> [Int]
incrementAllBy xs n =
  if null xs then []
  else (n + head xs):(incrementAllBy (tail xs) n)

incrementAllBy' :: [Int] -> Int -> [Int]
incrementAllBy' []     _ = []
incrementAllBy' (x:xs) n =
  (n + x):incrementAllBy' xs n

-- [1,2,3,4]
-- (x1:x2:xs) -> x1 = 1, x2 = 3, xs = [3, 4]
-- (x:xs) -> x = 1, xs = [2, 3, 4]
-- xs -> xs = [1, 2, 3, 4]

multiplyAllBy :: [Int] -> Int -> [Int]
multiplyAllBy []     _ = []
multiplyAllBy (x:xs) n = (n * x):multiplyAllBy xs n

filterSmallerThan :: [Int] -> Int -> [Int]
filterSmallerThan xs n
  | xs == [] = []
  | head xs >= n = head xs:filterSmallerThan (tail xs) n
  | otherwise    = filterSmallerThan (tail xs) n

filterSmallerThan' :: [Int] -> Int -> [Int]
filterSmallerThan' []     _ = []
filterSmallerThan' (x:xs) n =
  if x >= n 
  then x:filterSmallerThan' xs n
  else filterSmallerThan' xs n

-- List Comprehension
filterSmallerThan'' :: [Int] -> Int -> [Int]
filterSmallerThan'' xs n = [x | x <- xs, x >= n]

toList :: Int -> [Int]
toList n = helper n []
  where
    helper k res =
      if k < 10 then k:res
      else helper (k `div` 10) (mod k 10 : res)

check :: [Int] -> Bool
check []         = True
check [_]        = True
check (x1:x2:xs) = x1 < x2 && check (x2:xs)

isAscending :: Int -> Bool
isAscending n = check (toList n)

digits :: String -> String
digits str = [c | c <- str, isDigit c]

digitsSum' :: String -> Int
digitsSum' "" = 0
digitsSum' (c:cs) =
  (if isDigit c then ord c - ord '0' else 0) +
    digitsSum' cs

digitsSum :: String -> Int
digitsSum str =
  sum [ord c - ord '0' | c <- str, isDigit c]

capitalize :: String -> String
capitalize str = [toUpper c | c <- str]

isCapitalized :: String -> Bool
isCapitalized str = str == capitalize str