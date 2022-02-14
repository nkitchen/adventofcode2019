#!/usr/bin/env python3

import fileinput
import intcode
import os
import sys
from collections import Counter
from fractions import Fraction
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")
PROGRESS = os.environ.get("PROGRESS")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

view = None

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    slope_count = Counter()
    for x in range(1, 50):
        for y in range(1, 50):
            slope = Fraction(y, x)
            slope_count[slope] += 1

    min_pulled = None
    for slope in sorted(slope_count):
        x = slope.denominator
        y = slope.numerator
        p = intcode.Process(program)
        p.write(x)
        p.write(y)
        if p.read():
            min_pulled = slope
            break

    max_pulled = None
    for slope in sorted(slope_count, reverse=True):
        x = slope.denominator
        y = slope.numerator
        p = intcode.Process(program)
        p.write(x)
        p.write(y)
        if p.read():
            max_pulled = slope
            break

    print(min_pulled, max_pulled)

    pulled = 1
    for slope, n in slope_count.items():
        if min_pulled <= slope <= max_pulled:
            pulled += n

    print(pulled)

main()
