main :: IO()
main = do
  print 123
  print "abc"
  print a
  print (a + 10)
  print (f1 10 a)
  print (Main.min 12 10)
  print (Prelude.min 12 10)
  print (myfib' 0)
  print (myfib' 1)
  print (myfib' 2)
  print (myfib' 3)
  print (myfib' 4)
  print (myfib' 5)
  print (myfib' 500)
  print (f2 10)
  print (f1 10 20)
  print ((f1 10) 20)
  print (10 `f1` 20)
  print (mod 13 5)
  print (13 `mod` 5)
  print (12 + 5)
  print ((+) 12 5)
  print (mymaxdivisor 14)
  print (sumOddsInRange 1 10)
  print (sumOddsInRange' 1 10)
  print (isPrime 2)
  print (isPrime 4)
  print (isPrime 13)
  print (reverseNumber 1234)
  print (isPalindrome 12321)
  print (isPalindrome 123221)
  print (countPalindromes 1 100)
  print (10 / 3)
  print (10 `div` 3)
  print (countDivsIter 14)

a :: Int
a = 12

-- comment
{-
  multiple
  lines
-}

f1 :: Int -> Int -> Int
f1 a b = a * (2 + b)

-- Int, Integer, Float, Double, Char, String, Bool
-- Bool === True || False
-- &&, ||, not
-- +, -, *, /, ^, 
-- <, <=, >, >=, ==, /=

min :: Double -> Double -> Double
min a b =
  if a < b then a else b

isInside :: Int -> Int -> Int -> Bool
isInside x a b
  | x < a     = False
  | x > b     = False
  | otherwise = True

isInside' :: Int -> Int -> Int -> Bool
isInside' x a b = a <= x && x <= b

myfunc :: Double -> Double -> Double
myfunc a b = (a ^ 2 + b ^ 2) / 2

myfib :: Integer -> Integer
myfib n =
  if n <= 1 then 1 else myfib (n - 2) + myfib (n - 1)

myfib' :: Integer -> Integer
myfib' n = helper 0 0 1
  where
    helper i prev cur =
      if i == n then cur
      else helper (i + 1) cur (prev + cur)

f2 :: Int -> Int
f2 a = (a + b) * (g c)
  where
    b = 2 * a
    c = a + 5
    g x = b + x * 2


mymaxdivisor :: Int -> Int
mymaxdivisor x = helper (x - 1)
  where
    helper d =
      if x `mod` d == 0 then d
      else helper (d - 1)

sumOddsInRange :: Int -> Int -> Int
sumOddsInRange a b = helper a
  where
    helper a
      | a > b     = 0
      | odd a     = a + helper (a + 1)
      | otherwise = helper (a + 1)

sumOddsInRange' :: Int -> Int -> Int
sumOddsInRange' a b = helper a 0
  where
    helper a res
      | a > b     = res
      | odd a     = helper (a + 1) (res + a)
      | otherwise = helper (a + 1) res

isPrime :: Int -> Bool
isPrime n
  | n == 1 = False
  | n == 2 = True
  | otherwise = helper 2
  where
    helper d
      | d == n = True
      | mod n d == 0 = False
      | otherwise = helper (d + 1)

isPrime' :: Int -> Bool
isPrime' 1 = False
isPrime' 2 = True
isPrime' n = helper 2
  where
    helper d
      | d == n = True
      | mod n d == 0 = False
      | otherwise = helper (d + 1)


reverseNumber :: Int -> Int
reverseNumber n = helper n 0
  where
    helper k res =
      if k < 10 then res * 10 + k
      else helper (k `div` 10) (res * 10 + k `mod` 10)

isPalindrome :: Int -> Bool
isPalindrome n = n == reverseNumber n

countPalindromes :: Int -> Int -> Int
countPalindromes a b
  | a > b          = 0
  | isPalindrome a = 1 + countPalindromes (a + 1) b
  | otherwise      = countPalindromes (a + 1) b

countDivsIter :: Int -> Int
countDivsIter n = helper n 0
  where
    helper 0 count = count
    helper d count =
      if mod n d == 0 then helper (d - 1) (count + 1)
      else helper (d - 1) count 