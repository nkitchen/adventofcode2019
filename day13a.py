#!/usr/bin/env python3

import fileinput
import intcode
import os
from collections import defaultdict
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
PROGRESS = os.environ.get("PROGRESS")

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    screen = defaultdict(int)

    game = intcode.Process(program)
    while True:
        x = game.read()
        if x is None:
            break
        y = game.read()
        tile = game.read()
        screen[(x,y)] = tile

    blocks = sum(x == BLOCK for x in screen.values())
    print(blocks)

def display(screen):
    char = {
        EMPTY: '.',
        WALL: '+',
        BLOCK: '#',
        PADDLE: '=',
        BALL: '@',
    }

    xMin = min(x for x, y in screen)
    xMax = max(x for x, y in screen)
    yMin = min(y for x, y in screen)
    yMax = max(y for x, y in screen)
    for y in range(yMax, yMin - 1, -1):
        for x in range(xMin, xMax + 1):
            print(char[screen[(x,y)]], end='')
        print()

main()
