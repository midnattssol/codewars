#!/usr/bin/env python3.11
"""Performant solution for the coloured triangle problem.

https://www.codewars.com/kata/5a331ea7ee1aae8f24000175
"""
import math
import numpy as np

encoder = {"R": 0b011, "G": 0b110, "B": 0b101}
tri_2 = lambda r0, r1: (r0 & r1) ^ 0b111 * (r0 != r1)


def triangle(row):
    row = list(map(encoder.get, row))
    row = np.array(row)

    def inner(row):
        # n is always a natural number, the 0.01 is to
        # prevent off-by-one errors when it comes to
        # exact powers of 3. it is a very hacky solution though!
        n = len(row)
        dx = 3 ** int(math.log(n - 0.01, 3))

        if len(row) < 10:
            # Do the naive solution if the row is narrow enough
            while len(row) > 1:
                row = tri_2(row[:-1], row[1:])
            return row[0]

        out = tri_2(row[:-dx], row[dx:])
        assert len(out) < len(row)
        return inner(out)

    return {v: k for k, v in encoder.items()}[inner(row)]
