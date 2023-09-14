-- https://www.codewars.com/kata/5dd462a573ee6d0014ce715b

module CheckSameCase (sameCase) where
import Data.Char

sameCase :: Char -> Char -> Int

sameCase l r
    | not (isLetter(l) && isLetter(r)) = -1
    | isUpper(l) == isUpper(r) = 1
    | otherwise = 0
