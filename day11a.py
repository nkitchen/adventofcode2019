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

    robot = intcode.Process(program)
    while True:
        robot.write(panel[(x,y)])
        color = robot.read()
        if color is None:
            break
        turn = robot.read()

        panel[(x,y)] = color
        painted.add((x, y))
        if turn == LEFT:
            dx, dy = -dy, dx
        else:
            assert turn == RIGHT
            dx, dy = dy, -dx
        x += dx
        y += dy

    print(len(painted))

main()
