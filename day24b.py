#!/usr/bin/env python3

import fileinput
import os
import sys
from collections import Counter
from collections import namedtuple
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

def main():
    bugs = read_grid(fileinput.input())

    minutes = int(os.environ.get("MIN", 200))
    for t in range(minutes):
        bugs = advance(bugs)

    print(len(bugs))

class Loc(namedtuple('Loc', 'level x y')):
    def adjacent(self):
        # West
        if self.x == 0:
            yield Loc(self.level - 1, 1, 2)
        elif self.x == 3 and self.y == 2:
            for yy in range(5):
                yield Loc(self.level + 1, 4, yy)
        else:
            yield Loc(self.level, self.x - 1, self.y)

        # East
        if self.x == 4:
            yield Loc(self.level - 1, 3, 2)
        elif self.x == 1 and self.y == 2:
            for yy in range(5):
                yield Loc(self.level + 1, 0, yy)
        else:
            yield Loc(self.level, self.x + 1, self.y)

        # North
        if self.y == 0:
            yield Loc(self.level - 1, 2, 1)
        elif self.x == 2 and self.y == 3:
            for xx in range(5):
                yield Loc(self.level + 1, xx, 4)
        else:
            yield Loc(self.level, self.x, self.y - 1)

        # South
        if self.y == 4:
            yield Loc(self.level - 1, 2, 3)
        elif self.x == 2 and self.y == 1:
            for xx in range(5):
                yield Loc(self.level + 1, xx, 0)
        else:
            yield Loc(self.level, self.x, self.y + 1)

def advance(bugs):
    neighbors = Counter()
    for b in bugs:
        neighbors.update(b.adjacent())

    new_bugs = set()
    for loc, k in neighbors.items():
        if loc in bugs and k == 1:
            new_bugs.add(loc)
        elif loc not in bugs and k in [1, 2]:
            new_bugs.add(loc)
    return new_bugs

def show(bugs):
    levels = sorted(set(loc.level for loc in bugs))
    for level in levels:
        dprint(f"Depth {level}:")
        for y in range(0, 5):
            for x in range(0, 5):
                if x == 2 and y == 2:
                    dprint("?", end="")
                elif Loc(level, x, y) in bugs:
                    dprint("#", end="")
                else:
                    dprint(".", end="")
            dprint()
        dprint()

def read_grid(f):
    bugs = set()
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            if c == '#':
                bugs.add(Loc(0, x, y))
    return bugs

main()
