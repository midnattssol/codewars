#!/usr/bin/env python3.11
"""Solve a 5x5 nonogram.

https://www.codewars.com/kata/5a479247e6be385a41000064
"""
import dataclasses as dc
import itertools as it

import numpy as np


def ones(bits):
    return (*(sum(group) for bit, group in it.groupby(bits) if bit),)


def nonogram(size, clues_y, clues_x):
    possibilities = [[i for i in it.product(range(2), repeat=size) if ones(i) == c] for c in clues_x]

    return next(
        x for x in it.product(*possibilities) if all(ones(np.array(x)[:, i]) == c for i, c in enumerate(clues_y))
    )


@dc.dataclass
class Nonogram:
    clues: ...

    def solve(self):
        return nonogram(
            len(self.clues[0]),
            self.clues[0],
            self.clues[1],
        )
