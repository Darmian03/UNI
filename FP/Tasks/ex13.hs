import Data.List
import Data.Char

main :: IO()
main = do
  print (matching "1234" == [])
  print (matching ",[.[-],]" == [(1,7),(3,5)])
  print (matching ",+[-.,+]" == [(2,7)])
  print (matching "[][]" == [(0,1),(2,3)])
  print (prodEvens [1,2,3,4,5,6] == 15)
  print (prodEvens [7.66,7,7.99,7] == 61.2034)
  print ((switchsum (+ 1) (* 2) 1) 1)
  print ((switchsum (+ 1) (* 2) 2) 1)
  print ((switchsum (+ 1) (* 2) 3) 1)
  print ((switchsum (+ 1) (* 2) 4) 1)
  print (zip [0..] "abc")
  print (isImage [1,2,3] [3,4,5])
  print (isImage [1,2,3] [3,4,6])
  print (closestToAverage store1)
  print (cheaperAlternative store2)
  print (cheaperAlternative' store2)
  print ((numAdvance 5) [10, 9, 8, 7, 7, 7, 5, 5])
  print ((numAdvance 5) [10, 9, 8, 7, 7, 7, 5, 5] == 6)
  print ((numAdvance 2) [0, 0, 0, 0] == 0)
  print ((numAdvance 3) [10, 9, 8, 7, 7, 7, 5, 5] == 3)
  print ((numAdvance 1) [10, 9, 8, 7, 7, 7, 5, 5] == 1)
  print ((numAdvance 2) [10, 9, 8, 7, 7, 7, 5, 5] == 2)
  print ((numAdvance 9) [5, 5, 5, 3, 3, 3, 0, 0, 0, 0] == 6)
  print ((numAdvance 10) [5, 5, 5, 3, 3, 3, 0, 0, 0, 0] == 6)
  print (controller ""                       == "")
  print (controller ".........."             == "0000000000")
  print (controller "P...."                  == "12345")
  print (controller "P.P.."                  == "12222")
  print (controller "..P...O..."             == "0012343210")
  print (controller "P......P......"         == "12345554321000")
  print (controller "P.P.P...."              == "122234555")
  print (controller ".....P.P........P...."  == "000001222222222234555")
  print (controller ".........."             == "0000000000")
  print (controller "P.."                    == "123")
  print (controller "P...."                  == "12345")
  print (controller "P......P......"         == "12345554321000")
  print (controller "P.P.."                  == "12222")
  print (controller "P.P.P...."              == "122234555")
  print (controller ".....P.P........P...."  == "000001222222222234555")
  print (controller ".....P......P.P..P...." == "0000012345554333321000")
  print (controller "P.O...."                == "1210000")
  print (controller "P......P.O...."         == "12345554345555")
  print (controller "P..OP..P.."             == "1232222100")
  print (controller "P......P..OP..P..."     == "123455543233334555")
  print (controller "..P...O....."           == "001234321000")
  print (longestSubstring "aaabbcccccdde")
  print (group "aaabbcccccddeaa")
  print ((maximize [(\x -> x*x*x),(\x -> x+1)]) 0.5)
  print ((maximize [(\x -> x*x*x),(\x -> x+1)]) (-2))

matching :: String -> [(Int, Int)]
matching = helper . zip [0..]
  where
    helper []            = []
    helper ((i, '['):xs) = (i, closing 0 xs):helper xs
    helper (_:xs)        = helper xs

    closing 0 ((i, ']'):_)  = i
    closing k ((_, '['):xs) = closing (k + 1) xs
    closing k ((_, ']'):xs) = closing (k - 1) xs
    closing k (_:xs)        = closing k xs

prodEvens :: Num a => [a] -> a
prodEvens =
  foldr (*) 1 .
  (map snd) .
  (filter (\ (i, _) -> even i)) .
  (zip [0..])

switchsum :: Num a => (a -> a) -> (a -> a) -> Int -> (a -> a)
switchsum f g n = \ x -> helper f g 0 x
  where
    helper f g i x =
      if i == n then 0
      else f x + helper g f (i + 1) (f x)

isImage :: [Int] -> [Int] -> Bool
isImage as bs = length (group (zipWith (\ a b -> a - b) as bs)) == 1

store1 = [("bread", 1), ("milk", 2.5), ("lamb", 10),
          ("cheese", 5), ("butter", 2.3)]
store2 = [("bread", 1), ("cheese", 2.5), ("bread", 1),
          ("cheese", 5),("butter", 2.3)]

type Product = (String,Double)
type StoreAvailability = [Product]

closestToAverage :: StoreAvailability -> String
closestToAverage store =
  snd (minimum [(abs (p - averagePrice), n) | (n, p) <- store])
  where
    mean xs = sum xs / fromIntegral (length xs)
    averagePrice = mean [p | (_, p) <- store]

cheaperAlternative :: StoreAvailability -> Int
cheaperAlternative =
  length .
  filter (> 1) .
  (map length) .
  (map group) .
  (map (map snd)) .
  groupBy (\ (n1, _) (n2, _) -> n1 == n2) .
  sort

cheaperAlternative' :: StoreAvailability -> Int
cheaperAlternative' =
  length .
  filter (> 1) .
  map (length . group . map snd) .
  groupBy (\ (n1, _) (n2, _) -> n1 == n2) .
  sort

numAdvance :: (Ord a, Num a) => Int -> ([a] -> Int)
numAdvance k as = length [a | a <- as, a >= kthPoints, a > 0]
  where
    kthPoints = if k > length (filter (> 0) as) then 0 else as !! (k - 1)

controller :: String -> String
controller = (map intToDigit) . tail . reverse . fst3 . (foldl process ([0], 0, 0))
  where
    process (ms@(m:_), dir, act) '.' = ((constrain (m + dir * act)):ms, dir, act)
    process (ms@(m:_), dir, act) 'O' = ((constrain (m - dir * act)):ms, -dir, act)
    process (ms@(5:_), _,   _)   'P' = (4:ms, -1, 1)
    process (ms@(0:_), _,   _)   'P' = (1:ms, 1, 1)
    process (ms@(m:_), dir, 1)   'P' = (m:ms, dir, 0)
    process (ms@(m:_), dir, 0)   'P' = ((constrain (m + dir)):ms, dir, 1)
    
    constrain pos = if pos < 0 then 0 else if pos > 5 then 5 else pos
    
    fst3 (a, _, _) = a

longestSubstring :: String -> Int
longestSubstring = maximum . (map length) . group

maximize :: (Ord a, Num a) => [(a -> a)] -> (a -> a)
maximize fs = \ x ->
  (snd . maximum) [(abs fx, fx) | fx <- [f x | f <- fs]]
