#!/usr/bin/env python3

import fileinput
import os
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

def main():
    grid = read_grid(fileinput.input())

    layouts = set()
    while grid.bits not in layouts:
        layouts.add(grid.bits)
        grid = grid.advance()

    grid.dprint()

    rating = 0
    for i in range(25):
        b = 1 << i
        if grid.bits & b:
            rating += b

    print(rating)

class Grid():
    def __init__(self):
        self.bits = 0

    def __getitem__(self, xy):
        x, y = xy

        if x < 0 or x >= 5:
            return False
        if y < 0 or y >= 5:
            return False

        i = 5 * y + x
        return bool(self.bits & (1 << i))

    def __setitem__(self, xy, b):
        x, y = xy
        i = 5 * y + x
        if b:
            self.bits |= 1 << i
        else:
            self.bits &= ~(1 << i)

    def dprint(self):
        s = ""
        for y in range(0, 5):
            for x in range(0, 5):
                if self[x, y]:
                    s += "#"
                else:
                    s += "."
            s += "\n"
        dprint(s)

    def advance(self):
        succ = Grid()

        for x in range(0, 5):
            for y in range(0, 5):
                b = self[x, y]
                n = 0
                for nbr in adjacent(x, y):
                    n += int(self[nbr])
                if b and n == 1:
                    succ[x, y] = True
                if not b and n in [1, 2]:
                    succ[x, y] = True
        return succ

def adjacent(x, y):
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x, y - 1)
    yield (x, y + 1)

def read_grid(f):
    grid = Grid()
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            if c == '#':
                grid[x, y] = True
    return grid

main()
