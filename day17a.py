#!/usr/bin/env python3

import fileinput
import intcode
import os
import sys
from collections import defaultdict
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

    view = defaultdict(lambda: '.')
    p = intcode.Process(program)
    x = 0
    y = 0
    for c in p.outputs:
        if c == 10:
            y += 1
            x = 0
        else:
            view[(x, y)] = chr(c)
            x += 1

    m = max(view)
    if SHOW:
        for x in range(m[0] + 1):
            for y in range(m[1] + 1):
                print(view[(x, y)], end=' ')
            print()

    intersections = []
    for x in range(m[0] + 1):
        for y in range(m[1] + 1):
            p = (x, y)
            if view[p] == '#' and all(view[n] == '#' for n in neighbors(p)):
                intersections.append(p)

    s = 0
    for p in intersections:
        param = p[0] * p[1]
        s += param
    print(s)

def neighbors(p):
    for d in [-1, 1]:
        yield p[0] + d, p[1]
        yield p[0], p[1] + d

main()
