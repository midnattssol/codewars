-- https://www.codewars.com/kata/54bf1c2cd5b56cc47f0007a1/

module Codwars.Kata.Duplicates where
import Data.Char (toLower)
import Data.List (nub)


duplicateCount :: String -> Int
duplicateCount = countDups . (map toLower)
    where
        -- Count number of duplicates along unique items in list with `nub`
        count items item = length (filter (== item) items)
        countDups z = length (filter ((> 1) . (count z)) (nub z))
