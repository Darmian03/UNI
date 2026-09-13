main :: IO()
main = do
  print 11
  print s1
  print (Triangle 3 4 5)
  print pi
  print (perimeter s1)
  print (area s1)
  print (area (Triangle 3 4 5))
  print (sumArea [Rectangle 2 5, Rectangle 2 3])
  print (biggestShape [Rectangle 2 5, Rectangle 2 3])
  print (size t1)
  print (height t1)
  print (sumLeaves t1)
  print (inorder t1)
  print (getLevel 0 t1)
  print (getLevel 1 t1)
  print (getLevel 2 t1)
  print (getLevel 3 t1)
  print (average t1)
  print (mirrorTree t3)

data Shape = Circle Double | Rectangle Double Double | Triangle Double Double Double
  deriving (Eq, Ord)

instance Show Shape where
  show (Circle r) = "Circle with r = " ++ show r
  show (Rectangle a b) = "Rectangle with sides a = " ++ show a ++ " and b = " ++ show b
  show (Triangle a b c) = show a ++ ", " ++ show b ++ ", " ++ show c

s1 :: Shape
s1 = Rectangle 10 15

perimeter :: Shape -> Double
perimeter (Circle r) = 2 * pi * r
perimeter (Rectangle a b) = 2 * (a + b)
perimeter (Triangle a b c) = a + b + c

area :: Shape -> Double
area (Circle r) = pi * r * r
area (Rectangle a b) = a * b
area (Triangle a b c) = sqrt (p * (p - a) * (p - b) * (p - c))
  where p = (a + b + c) / 2

sumArea :: [Shape] -> Double
sumArea = sum . (map area)

biggestShape :: [Shape] -> Shape
biggestShape ss = (snd . maximum) [(area s, s) | s <- ss]

data BTree = Empty | Node Int BTree BTree
  deriving (Show, Eq)

t1 :: BTree                               --    5
t1 = Node 5 (Node 2 Empty                 --   / \
                    (Node 3 Empty Empty)) --  2   6
            (Node 6 Empty Empty)          --   \
                                          --    3 

t2 :: BTree                               --    5
t2 = Node 5 (Node 3 Empty Empty)          --   / \
            (Node 4 (Node 5 Empty Empty)  --  3   4
                    (Node 7 Empty Empty)) --     / \
                                          --    5   7

size :: BTree -> Int
size Empty = 0
size (Node _ lt rt) = 1 + size lt + size rt

height :: BTree -> Int
height Empty = 0
height (Node _ lt rt) = 1 + max (height lt) (height rt)

sumTree :: BTree -> Int
sumTree Empty = 0
sumTree (Node v lt rt) = v + sumTree lt + sumTree rt

sumLeaves :: BTree -> Int
sumLeaves Empty = 0
sumLeaves (Node v Empty Empty) = v
sumLeaves (Node _ lt rt) = sumLeaves lt + sumLeaves rt

inorder :: BTree -> [Int]
inorder Empty = []
inorder (Node v lt rt) = inorder lt ++ [v] ++ inorder rt

getLevel :: Int -> BTree -> [Int]
getLevel _ Empty = []
getLevel 0 (Node v _ _) = [v]
getLevel k (Node _ lt rt) =
  getLevel (k - 1) lt ++ getLevel (k - 1) rt

average :: BTree -> Double
average bt =
  fromIntegral (sumTree bt) / fromIntegral (size bt)

t3 :: BTree                               --     1
t3 = Node 1 (Node 2 (Node 5 Empty Empty)  --    / \
                    Empty)                --   2   3
            (Node 3 (Node 7 Empty Empty)  --  /   / \
                    (Node 6 Empty Empty)) -- 5   7   6

mirrorTree :: BTree -> BTree
mirrorTree Empty = Empty
mirrorTree (Node v lt rt) =
  Node v (mirrorTree rt) (mirrorTree lt)