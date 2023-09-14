#!/usr/bin/env python3.11
"""Solve a sudoku.

https://www.codewars.com/kata/5296bc77afba8baa690002d7/
"""
import itertools as it


def sudoku(board):
    def propagate(pos, value):
        options.pop(pos)
        board[pos[0]][pos[1]] = value
        square = [(3 * (i // 3), 3 * (i // 3 + 1)) for i in pos]
        to_update = {*it.product(*it.starmap(range, square))}
        to_update |= {(pos[0], i) for i in range(9)}
        to_update |= {(i, pos[1]) for i in range(9)}
        to_update &= set(options)

        for new_index in to_update:
            options[new_index] -= {value}

        return to_update

    queue = [*it.product(range(9), repeat=2)]
    options = {k: {*range(1, 10)} for k in queue}

    for x, y in filter(lambda c: board[c[0]][c[1]], queue):
        propagate((x, y), board[x][y])

    while queue:
        index = queue.pop()

        if (opt := options.get(index)) is not None and len(opt) == 1:
            affected = propagate(index, next(iter(opt)))
            queue = affected.union(queue).intersection(options)
            queue = list(queue)

    return board
