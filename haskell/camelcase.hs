module Codewars.Kata.BreakCamelCase where
import Data.Char


solution item = dropWhile isSpace (foldl (++) "" (map solution2 item))
    where
    solution2 char
        | isUpper(char) = [' ', char]
        | otherwise = [char]
