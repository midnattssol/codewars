-- https://www.codewars.com/kata/5842df8ccbd22792a4000245

module Kata where


expandedForm :: Int -> String
expandedForm n
    | n < 10 = show n
    | nModK == 0 = show (n - nModK)
    | otherwise = show (n - nModK) ++ " + " ++ expandedForm nModK
        where
            k = 10 ^ floor (logBase 10 (fromIntegral n))
            nModK = mod n k
