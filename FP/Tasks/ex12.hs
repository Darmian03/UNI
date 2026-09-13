import Data.List

main :: IO()
main = do
  print (sumTree t1)
  print (sumTree t2)
  print (t1 == Node 5 Empty Empty)
  --print (t1 == t2)
  print (getLevelsTree t1)
  print (mapTree (* 2) t1)
  print (maxDepthBlueNode colorTree)
  print (maxDepthBlueNode' colorTree)
  print (maxDepthNode colorTree Blue)
  print (maxDepthNode' colorTree Blue)
  print (maxDepthNode'' colorTree Blue)
  print (size nTree1)
  print (isGracious nTree1)
  print (isGracious nTree2)
  print (all even [])
  print (and [])
  print (twoChildrenNodes at1)
  print (findUncles at1 3)

data BTree a = Empty | Node a (BTree a) (BTree a)
  deriving (Show, Eq)

t1 :: BTree Int                           --    5
t1 = Node 5 (Node 2 Empty                 --   / \
                    (Node 3 Empty Empty)) --  2   6
            (Node 6 Empty Empty)          --   \
                                          --    3 

t2 :: BTree Double
t2 = Node 5.1 (Node 2.2 Empty
                    (Node 3.3 Empty Empty))
              (Node 6.4 Empty Empty)

sumTree :: Num a => BTree a -> a
sumTree Empty          = 0
sumTree (Node v lt rt) = v + sumTree lt + sumTree rt

getLevelsTree :: BTree a -> BTree (a, Int)
getLevelsTree = helper 0
  where
    helper _ Empty = Empty
    helper k (Node v lt rt) =
      Node (v, k) (helper (k + 1) lt) (helper (k + 1) rt)

mapTree :: (a -> b) -> BTree a -> BTree b
mapTree _ Empty = Empty
mapTree f (Node v lt rt) =
  Node (f v) (mapTree f lt) (mapTree f rt)

data Color = Red | Green | Blue deriving (Read, Show, Eq)
colorTree :: BTree Color                                            --            Blue
colorTree = Node Blue (Node Red (Node Green Empty Empty) Empty)     --           /    \
                      (Node Red (Node Blue (Node Green Empty Empty) --        Red      Red
                                           (Node Red Empty Empty))  --        /        /  
                                Empty)                              --     Green     Blue  
                                                                    --               /   \
                                                                    --            Green  Red
maxDepthBlueNode :: BTree Color -> Int
maxDepthBlueNode = helper 0
  where
    helper _ Empty = -1
    helper k (Node Blue lt rt) =
      maximum [k, helper (k + 1) lt, helper (k + 1) rt]
    helper k (Node _ lt rt) =
      max (helper (k + 1) lt) (helper (k + 1) rt)

inorder :: BTree a -> [a]
inorder Empty = []
inorder (Node v lt rt) = inorder lt ++ v : inorder rt

maxDepthBlueNode' :: BTree Color -> Int
maxDepthBlueNode' bt =
  maximum [k | (Blue, k) <- inorder (getLevelsTree bt)]

maxDepthNode :: BTree Color -> Color -> Int
maxDepthNode = helper 0
  where
    helper _ Empty          _     = -1
    helper k (Node v lt rt) color =
      if v == color
      then maximum [k,
                    helper (k + 1) lt color,
                    helper (k + 1) rt color]
      else max (helper (k + 1) lt color)
               (helper (k + 1) rt color)

maxDepthNode' :: BTree Color -> Color -> Int
maxDepthNode' bt color = helper 0 bt
  where
    helper _ Empty = -1
    helper k (Node v lt rt) =
      if v == color
      then maximum [k,
                    helper (k + 1) lt,
                    helper (k + 1) rt]
      else max (helper (k + 1) lt)
               (helper (k + 1) rt)

maxDepthNode'' :: BTree Color -> Color -> Int
maxDepthNode'' bt color =
  maximum [k | (v, k) <- inorder (getLevelsTree bt), v == color]

data NTree a = NEmpty | NNode a [NTree a]
  deriving Show

nTree1 :: NTree Int                               --       1
nTree1 = NNode 1 [(NNode 2 [(NNode 3 [NEmpty]),   --      / \
                            (NNode 4 [NEmpty]),   --     2   6
                            (NNode 5 [NEmpty])]), --    /|\  |
                  (NNode 6 [(NNode 7 [NEmpty])])] --   3 4 5 7

nTree2 :: NTree Int                               --       1
nTree2 = NNode 1 [(NNode 3 [(NNode 3 [NEmpty]),   --      / \
                            (NNode 5 [NEmpty]),   --     3   5
                            (NNode 7 [NEmpty])]), --    /|\  |
                  (NNode 5 [(NNode 7 [NEmpty])])] --   3 5 7 7


size :: NTree a -> Int
size NEmpty = 0
size (NNode _ ts) = 1 + sum (map size ts)

isGracious :: NTree Int -> Bool
isGracious NEmpty = True
isGracious (NNode v ts) =
  all even [v - u | (NNode u _) <- ts] && all isGracious ts

--  and [even (v - u) | (NNode u _) <- ts]

at1 = [(4, [2, 5]), (2, [1, 3])]
--     4
--    / \
--   2   5
--  / \
-- 1   3

twoChildrenNodes :: [(a, [a])] -> Int
twoChildrenNodes ats =
  length [v | (v, us) <- ats, length us == 2]

findUncles :: Eq a => [(a, [a])] -> a -> [a]
findUncles tree node = 
  delete father (head [us | (_, us) <- tree, elem father us])
  where
    father = head [v | (v, us) <- tree, elem node us]