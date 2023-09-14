#!/usr/bin/env python3.11
"""Compute a binomial expansion.

https://www.codewars.com/kata/540d0fdd3b6532e5c3000b5b
"""
import re
from math import factorial


def choose(k, n):
    return factorial(k) // (factorial(n) * factorial(k - n))


def expand(expression):
    a = re.match(r"\((-?\d*)(\w)([+-]\d+)\)\^(\d+)", expression)

    coeff, varname, num, power = a.groups()
    coeff = coeff + "1" * bool(coeff.strip("-"))
    coeff = int(coeff)

    num = int(num)
    power = int(power)
    factors = [num**n * coeff ** (power - n) * choose(power, n) for n in range(1, power + 1)]
    factors.insert(0, coeff**power)

    def term2str(x, power):
        if not x:
            return ""
        if not power:
            return f"{x:+d}"
        x = f"{x:+d}".strip("1" if abs(x) == 1 else "")
        return f"{x}{varname}" + (f"^{power}" if power != 1 else "")

    acc = [term2str(x, power - i) for i, x in enumerate(factors) if x]
    acc = "".join(acc).strip("+")
    return acc
