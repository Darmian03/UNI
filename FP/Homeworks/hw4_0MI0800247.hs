import Data.Char
import Data.List
import Data.Maybe

main :: IO()
main = do
  print "Task 1"
  print (reversibleNumbers 20 == [12,14,16,18])
  print (reversibleNumbers 31 == [12,14,16,18,21,23,25,27])
  print (reversibleNumbers 10 == [])

  print "Task 2"
  print ((findUniques db) 4  == ["SICP","Real World Haskell"])
  print ((findUniques db) 8  == ["Real World Haskell"])
  print ((findUniques db) 32 == [])

  print "Task 3"
  print (minCalibrationValue ["1abc2", "pqrthreestu8vwx", "a1b2c3d4e5f", "trebsevenuchet"] == "1abc2")
  print (minCalibrationValue ["has1ell", "rac5et"] == "has1ell")
  print (minCalibrationValue ["jboktwoneaad", "agga20zs"] == "agga20zs")
  print (minCalibrationValue ["jboktwoneaad", "agninega5zs"] == "jboktwoneaad")
  print (minCalibrationValue ["1hhdz156qpfmmrb", "onetwo6ctkntf", "pfthree3oneninegzqpgxq2eight", "four99", "8bcr"] == "onetwo6ctkntf")
  print (minCalibrationValue ["eight24five1", "k8two918hrnine", "948", "jnhldbh7dkskeight9", "np2"] == "np2")
  print (minCalibrationValue ["rkmbh8", "five3xhpsdfkg94two3six", "bcstq5dghsfrcmftwo4lflbbrpztwo", "fiveightjdd4eight", "7mmvkgmq"] == "bcstq5dghsfrcmftwo4lflbbrpztwo")

  print "Task 4"
  print (canSplitWord t1 "BDCGI"  == True)
  print (canSplitWord t1 "BDGI"   == True)
  print (canSplitWord t1 "BDCGIH" == True)
  print (canSplitWord t1 "BGIH"   == False)
  print (canSplitWord t1 "BCDGI"  == False)
  print (canSplitWord t1 "BDGH"   == False)

  where
    db = [("SICP",1996),("Learn You a Haskell for Great Good",2011),
          ("Real World Haskell",2008),("Programming in Haskell",2011)]

    t1 = Node 'F' (Node 'B' (Node 'A' NullT NullT)
                            (Node 'D' (Node 'C' NullT NullT)
                                      (Node 'E' NullT NullT)))
                  (Node 'G' NullT
                            (Node 'I' (Node 'H' NullT NullT)
                                      NullT))

-- Task 1
reversibleNumbers :: Int -> [Int]
reversibleNumbers n = [k | k <- [1..n], isReversable k]
  where
    reverseNumber k = read (reverse (show k)) :: Int
    isReversable k =
      mod k 10 /= 0 && all (odd . digitToInt) (show (k + reverseNumber k))


-- Task 2
findUniques :: [(String, Int)] -> (Int -> [String])
findUniques db =
  \ n -> [t | (t, y) <- db, length t >= n, not (elem y (delete y ys))]
  where ys = map snd db


-- Task 3
calibrationValue :: String -> Int
calibrationValue str = fstValue str * 10 + sndValue str
  where
    digitStrings = [("zero", 0), ("one", 1), ("two", 2), ("three", 3),
                    ("four", 4), ("five", 5), ("six", 6), ("seven", 7),
                    ("eight", 8), ("nine", 9)]

    findValue str@(c:cs) ds = 
      if isDigit c then ([c], digitToInt c)
      else fromMaybe (findValue cs ds)
                     (find (\ (w, n) -> isPrefixOf w str) ds)

    fstValue str = snd (findValue str digitStrings)

    sndValue str = snd (findValue (reverse str)
                                  (map (\ (s, d) -> (reverse s, d)) digitStrings))

minCalibrationValue :: [String] -> String
minCalibrationValue =
  fst .
  (foldl1 (\ d1@(_, v1) d2@(_, v2) -> if v1 < v2 then d1 else d2)) .
  map (\ s -> (s, calibrationValue s))


-- Task 4
data BTree = NullT | Node Char BTree BTree deriving Show

canSplitWord (Node _ lt rt) str =
  any (\ (ls, rs) -> isPath ls lt && isPath rs rt)
      [splitAt n str | n <- [2..length str - 2]]
  where
    isPath "" _  = True
    isPath _ NullT  = False
    isPath (a:as)  (Node c lt rt) = c == a && (isPath as lt || isPath as rt)