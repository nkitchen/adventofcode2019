#!/usr/bin/env python3

import fileinput
import os
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

def main():
    inp = fileinput.input()

    deck_size = int(next(inp))
    shuffle_iters = int(next(inp))
    target_position = int(next(inp))

    scale = 1
    offset = 0
    for line in inp:
        line = line.rstrip()
        if line == "deal into new stack":
            scale = -scale
            offset = -offset - 1
        elif (m := re.match(r"cut (-?\d+)", line)):
            N = int(m.group(1))
            offset -= N
        elif (m := re.match(r"deal with increment (\d+)", line)):
            N = int(m.group(1))
            scale *= N
            offset *= N

    a = scale
    b = offset
    p = shuffle_iters
    n = deck_size
    i = target_position
    # k = (a^-1)^p * (i - b*(1 - a^p)*(1 - a)^-1)
    # See analysis below.
    t1 = pow(pow(a, -1, n), p, n) % n
    t2 = b * (1 - pow(a, p, n)) * pow(1 - a, -1, n) % n
    k = t1 * (i - t2) % n
    print(k)

main()

analysis = """
Deck size is n.
Card k is at position i = (a*k + b) % n.
scale a, offset b

For simplicity, assume all calculations are ... % n.

Shuffle effects
===============
deal into new stack:
    j  = -i - 1
       = -(a*k + b) - 1
       = -a*k - b - 1
    a' = -a
    b' = -b - 1

cut N (any sign):
    j  = i - N
       = a*k + b - N
    a' = a
    b' = b - N

deal with increment N:
    j  = i * N
       = (a*k + b) * N
       = a*N*k + b*N
    a' = a * N
    b' = b * N

The sequence of shuffle steps results in a net scale a and offset b.

Iterating
=========
After 1 iteration, card k is at position a*k + b.
After 2 iterations, card k is at position a*(a*k + b) + b = a*a*k + a*b + b.
After 3 iterations, card k is at a*(a*a*k + a*b + b) + b
                               = a*a*a*k + a*a*b + a*b + b.
After p iterations, card k is at a^p*k + b*sum_{i=0}^{p-1}(a^i).

Modular geometric sum:
1 + a + ... + a^{p-1} + a^p = 1 + a * (1 + a + ... + a^{p-1})
(1 + a + ... + a^{p-1}) * (1 - a) = 1 - a^p
(1 + a + ... + a^{p-1}) * (1 - a) * (1 - a)^-1 = (1 - a^p) * (1 - a)^-1
1 + a + ... + a^{p-1} = (1 - a^p) * (1 - a)^-1

Card k is at a^p*k + b*(1 - a^p) * (1 - a)^-1.
a^p*k = i - b*(1 - a^p)*(1 - a)^-1
(a^-1)^p*a^p*k = (a^-1)^p * (i - b*(1 - a^p)*(1 - a)^-1)
k = (a^-1)^p * (i - b*(1 - a^p)*(1 - a)^-1)
"""
