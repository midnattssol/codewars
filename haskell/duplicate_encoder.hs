-- https://www.codewars.com/kata/54b42f9314d9229fd6000d9c/

module Dups where
import Data.Char

-- rolling my own count function for learning purposes :D
count :: Eq a => [a] -> a -> Int
count items item = foldl (+) 0 (map (fromEnum . (== item)) items)

preencode :: String -> Char -> Char
preencode items item
    | (count items item) > 1 = ')'
    | otherwise = '('


duplicateEncode :: String -> String
duplicateEncode items = map (preencode items2) items2
    where items2 = map toLower items
