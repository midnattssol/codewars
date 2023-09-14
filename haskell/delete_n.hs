-- https://www.codewars.com/kata/554ca54ffa7d91b236000023/

module Codewars.Kata.Deletion where
import qualified Data.Map.Strict as M


deleteNthIntermediate :: M.Map Int Int -> [Int] -> Int -> [Int]
deleteNthIntermediate occurrences lst n = case lst of
  (hd:rest)
    | (M.findWithDefault 0 hd occurrences) < n -> hd : newRest
    | otherwise -> newRest
    where
      -- Add 1 to the new occurrences, and recurse on the rest of the list.
      newOccurrences = M.insertWith (+) hd 1 occurrences
      newRest = deleteNthIntermediate newOccurrences rest n

  -- The base case - if the list is empty, return the empty list.
  [] -> []


deleteNth = deleteNthIntermediate M.empty
