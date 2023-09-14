#!/usr/bin/env python3.11
"""Count ones in a segment.

https://www.codewars.com/kata/596d34df24a04ee1e3000a25
"""


def count_ones(left, right):
    def inner(right):
        out = 0
        while right > 0:
            n_bits = len(bin(right)[2:]) - 1
            cutoff = 1 << n_bits
            out += (cutoff * n_bits) // 2
            out += right - cutoff + 1
            right -= cutoff

        return out

    return inner(right) - inner(left - 1)
