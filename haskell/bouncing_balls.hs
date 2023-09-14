-- https://www.codewars.com/kata/5544c7a5cb454edb3c000047/
module Codewars.Kata.BouncingBall where

bouncingBall :: Double -> Double -> Double -> Integer

-- It's obviously a lot more effective to just calculate the result numerically, but I think this is a good exercise in writing more complicated Haskell functions :)

bouncingBall dropHeight bounceFactor windowHeight
  | isValid = (toInteger . timesSeen . occurencesAbove) windowHeight
  | otherwise = -1
  where
      isValid = (dropHeight > 0) && (bounceFactor > 0) && (bounceFactor < 1) && (windowHeight < dropHeight)
      timesSeen x = (2 * x) - 1
      bounceHeights = iterate (* bounceFactor) dropHeight
      occurencesAbove windowHeight = length (takeWhile (> windowHeight) bounceHeights)
