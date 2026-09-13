import Data.List

main :: IO()
main = do
    print $ leavesAreEqual t1 t2 == True
    print $ leavesAreEqual t3 t4 == False

t1 = Node 10 (Node 1 Nil Nil) (Node 25 Nil (Node 30 (Node 26 Nil Nil) (Node 32 Nil Nil)))
t2 = Node 25 (Node 10 (Node 1 Nil Nil) Nil) (Node 30 (Node 32 Nil Nil) (Node 26 Nil Nil))
t3 = t1
t4 = Node 10 (Node 1 Nil Nil) (Node 25 Nil (Node 30 (Node 27 Nil Nil) (Node 32 Nil Nil)))

data BTree a = Nil | Node a (BTree a) (BTree a)

getLeaves :: BTree a -> [a]
getLeaves Nil = []
getLeaves (Node value Nil Nil) = [value]
getLeaves (Node _ left right) = getLeaves left ++ getLeaves right

leavesAreEqual :: (Eq a, Ord a) => BTree a -> BTree a -> Bool
leavesAreEqual tree1 tree2 = sort (getLeaves tree1) == sort (getLeaves tree2)
