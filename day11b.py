#!/usr/bin/env python3

import fileinput
import intcode
import itertools
import os
from collections import defaultdict
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
PROGRESS = os.environ.get("PROGRESS")

LEFT = 0
RIGHT = 1

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    panel = defaultdict(int)
    painted = set()
    x, y = 0, 0
    dx, dy = 0, 1
    panel[(x,y)] = 1

    robot = intcode.Process(program)
    while True:
        robot.write_in(panel[(x,y)])
        color = robot.read_out()
        if color is None:
            break
        turn = robot.read_out()

        panel[(x,y)] = color
        painted.add((x, y))
        if turn == LEFT:
            dx, dy = -dy, dx
        else:
            assert turn == RIGHT
            dx, dy = dy, -dx
        x += dx
        y += dy

    xMin = min(x for x, y in panel)
    xMax = max(x for x, y in panel)
    yMin = min(y for x, y in panel)
    yMax = max(y for x, y in panel)
    for y in range(yMax, yMin - 1, -1):
        for x in range(xMin, xMax + 1):
            if panel[(x,y)]:
                print('#', end='')
            else:
                print('.', end='')
        print()

main()
