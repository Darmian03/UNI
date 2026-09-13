import Data.List
import Data.Char

main :: IO()
main = do
    print (findMaxPalindrome 1112332)
    print (findMaxPalindrome 22220)
    print (findMaxPalindrome 2205)
    print (findMaxPalindrome 120021)
    print (findMaxPalindrome 12320)
    print (findMaxPalindrome 123)
    print (findMaxPalindrome 1002)
    print (calculate "1+2+x" [('x', 5)])
    print (calculate "x+2+x-2+y+z" [('x', 1), ('y', 2), ('z', 3)])
    print (calculate "x+2-x-2+y+x" [('x', 1), ('y', -15)])
    print (calculate "y+2+x-2+z+z+z+x+5" [('x', 1), ('y', 2), ('z', 3)])
    print (calculate "8-2" [])
    print (calculate "5" [])
    
-- ПЪРВА ЗАДАЧА
findMaxPalindrome :: Integer -> Integer
findMaxPalindrome n = (corrector (makeInteger (helper (reverse (sort (makelist n))) 0)))
    where
        corrector a =
            if (mod a 10) == 0 && a /= 0 then corrector (div a 10)
            else a
        
        makelist 0 = []
        makelist x = (mod x 10) : makelist (div x 10)

        makeInteger [] = 0
        makeInteger (x:xs) = x + 10*(makeInteger xs)

        helper xs a
            | null xs && a == 0                  = []
            | null xs                            = [a]
            | null (tail xs) && (head xs) >= a   = xs
            | null (tail xs)                     = [a]
            | (head xs) == (head (tail xs))      = [(head xs)] ++ (helper (drop 2 xs) a) ++ [(head xs)]
            | otherwise                          = (helper (tail xs) (max a (head xs)))

--ВТОРА ЗАДАЧА
calculate :: String -> [(Char, Int)] -> Int
calculate str var = helper 0 str var '+'
    where
        getValue _ [] = 0
        getValue a ((x, y) : xs) =
            if a == x then y
            else getValue a xs

        operator '+' x y = x + y
        operator '-' x y = x - y

        helper sum [] _ _ = sum
        helper sum (x : xs) var operation
            | x == '-'    = helper sum xs var '-'
            | x == '+'    = helper sum xs var '+'
            | isDigit x   = helper (operator operation sum (digitToInt x)) xs var operation
            | otherwise   = helper (operator operation sum (getValue x var)) xs var operation