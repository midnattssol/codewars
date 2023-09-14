-- https://www.codewars.com/kata/57a049e253ba33ac5e000212/

module Factorial where

factorial :: Int -> Int
factorial x = foldl (*) 1 [1..x]
