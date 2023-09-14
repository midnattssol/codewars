#!/usr/bin/env python3.11
"""Validate a Battleship playing board using dynamic programming.

https://www.codewars.com/kata/571ec81d7e8954ce1400014f
"""
import numpy as np


def find_ship_locations(arr, filter):
    # Does a convolution-like operation.
    out = np.zeros_like(arr)

    for i in range(arr.shape[0] - filter.shape[0]):
        for j in range(arr.shape[1] - filter.shape[1]):
            window = arr[i : i + filter.shape[0], j : j + filter.shape[1]]
            out[i, j] = np.sum(window & filter) == np.sum(filter)

    return np.array(np.where(out)).T


def validate_battlefield(battlefield):
    new_battlefield = np.zeros(np.array(np.array(battlefield).shape) + 2, dtype=np.int64)
    new_battlefield[1:-1, 1:-1] = battlefield
    battlefield = new_battlefield
    collapsed = battlefield.copy()

    def validate(collapsed, expected):
        # One-block ships always fit. There is a previous check for the number of squares,
        # so it isn't rechecked here.
        only_subs = len(expected) == 1 and next(iter(expected.keys())) == 1

        if (not any(expected.values())) or only_subs:
            return True

        for ship_size, n in expected.items():
            if n < 1:
                continue

            filters = [
                np.full((1, ship_size), 1),
                np.full((ship_size, 1), 1),
            ]

            for filter in filters:
                locations = find_ship_locations(collapsed, filter)

                # Count down one step since the ship was found.
                expected_ = expected.copy()
                expected_[ship_size] -= 1

                for index in locations:
                    collapsed[
                        index[0] : index[0] + filter.shape[0],
                        index[1] : index[1] + filter.shape[1],
                    ] ^= filter

                    # Recurse.
                    if validate(collapsed, expected_):
                        return True

                    collapsed[
                        index[0] : index[0] + filter.shape[0],
                        index[1] : index[1] + filter.shape[1],
                    ] ^= filter

            # More ships are expected, but none of them
            # can be placed in a valid spot.
            return False

    expected = {4: 1, 3: 2, 2: 3, 1: 4}

    # Check the number of occupied squares.
    if np.sum(battlefield) != sum(k * v for k, v in expected.items()):
        return False

    return validate(collapsed, expected)
