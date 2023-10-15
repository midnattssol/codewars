module Tribonacci where

tribonacci :: Num a => (a, a, a) -> Int -> [a]
tribonacci (a, b, c) n = [a, b, c] ++ inner (a, b, c) (n - 3)
    where
        next a b c = a + b + c
        inner (a, b, c) n
            | n == 0 = []
            | otherwise = next a b c : inner (b, c, next a b c) (n - 1)
