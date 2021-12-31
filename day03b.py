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

    steps = min(pts1[p] + pts2[p] for p in pts1.keys() & pts2.keys())
    print(steps)

    if DEBUG:
        pprint(sorted([(pts1[p] + pts2[p], p, pts1[p], pts2[p]) for p in pts1.keys() & pts2.keys()]))

def path_points(path):
    x, y = 0, 0
    t = 0
    steps = {}
    for inst in path:
        dir = inst[0:1]
        n = int(inst[1:])

        if dir == 'R':
            dx = 1
            dy = 0
        elif dir == 'L':
            dx = -1
            dy = 0
        elif dir == 'U':
            dx = 0
            dy = 1
        elif dir == 'D':
            dx = 0
            dy = -1

        for k in range(1, n + 1):
            x += dx
            y += dy
            t += 1
            p = (x, y)
            if p not in steps:
                steps[p] = t

    return steps

main()
