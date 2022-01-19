#!/usr/bin/env python3

import fileinput
import intcode
import os
import sys
import time
from collections import defaultdict
from pprint import pprint

DISPLAY = os.environ.get("DISPLAY")
PROGRESS = os.environ.get("PROGRESS")

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

LEFT = -1
RIGHT = 1
NEUTRAL = 0

def dprint(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    screen = defaultdict(int)

    game = intcode.Process(program)
    game.mem[0] = 2
    game.write(RIGHT)

    paddle_x = None
    ball_x = None

    while True:
        x = game.read()
        if x is None:
            break
        y = game.read()
        tile = game.read()

        if (x, y) == (-1, 0):
            score = tile
            continue

        screen[(x,y)] = tile

        if tile == PADDLE:
            paddle_x = x
        elif tile == BALL:
            ball_x = x

            if paddle_x is not None:
                if paddle_x > ball_x:
                    game.write(LEFT)
                elif paddle_x < ball_x:
                    game.write(RIGHT)
                else:
                    game.write(NEUTRAL)

            if DISPLAY:
                display(screen)
                time.sleep(0.05)
                #_ = input()

    print(score)

def display(screen):
    char = {
        EMPTY: '.',
        WALL: '+',
        BLOCK: '#',
        PADDLE: '=',
        BALL: '@',
    }

    try:
        os.ttyname(1)
        os.system("clear")
    except OSError:
        pass

    xMax = max(x for x, y in screen)
    yMax = max(y for x, y in screen)
    for y in range(yMax + 1):
        for x in range(xMax + 1):
            dprint(char[screen[(x,y)]], end='')
        dprint()

main()
