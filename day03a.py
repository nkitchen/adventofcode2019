#!/usr/bin/env python3

import fileinput
import itertools
import os
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    inp = fileinput.input()
    path1 = inp.readline().rstrip().split(',')
    path2 = inp.readline().rstrip().split(',')

    pts1 = path_points(path1)
    pts2 = path_points(path2)

    d = min(dist(p) for p in pts1 & pts2)
    print(d)

def path_points(path):
    x, y = 0, 0
    s = set()
    for step in path:
        dir = step[0:1]
        n = int(step[1:])

        if dir == 'R':
            t = itertools.product(range(x + 1, x + n + 1), [y])
            x += n
        elif dir == 'L':
            t = itertools.product(range(x - 1, x - n - 1, -1), [y])
            x -= n
        elif dir == 'U':
            t = itertools.product([x], range(y + 1, y + n + 1))
            y += n
        elif dir == 'D':
            t = itertools.product([x], range(y - 1, y - n - 1, -1))
            y -= n

        s |= set(t)

        if DEBUG:
            pprint(s)

    return s

def dist(p):
    return abs(p[0]) + abs(p[1])

main()
