#!/usr/bin/env python3.11
"""Get the number of a permutation of items in an ordered list of the permutations.

https://www.codewars.com/kata/53e57dada0cb0400ba000688
"""
import functools as ft
import operator as op
import collections as col


def factorial(x):
    return ft.reduce(op.mul, range(2, x + 1), 1)


def list_position(x):
    def inner(seq):
        if not seq:
            return 0
        n_perms = factorial(len(seq))
        n_perms //= ft.reduce(op.mul, map(factorial, col.Counter(seq).values()))
        return sorted(seq).index(seq[0]) * n_perms // len(seq) + inner(seq[1:])

    return inner(x) + 1
