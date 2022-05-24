#!/usr/bin/env python3

import fileinput
import intcode
import itertools
import math
import os
import sys
from collections import Counter
from fractions import Fraction
from pprint import pprint

# Given slopes a < b and distance d,
# find minimum integer x, y such that:
#     a <= y/(x + d)
#          (y + d)/x <= b
#
# I don't assume that I can get exact values for a and b from the 50x50 grid
# as in part 1.
# Instead, I find loose lower and upper bounds (the closest slopes *outside*
# the tractor beam), fit a d-x-d square exactly to those, and then shift it
# until it fits inside the beam.

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")
PROGRESS = os.environ.get("PROGRESS")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

view = None

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    d = 99

    def pulled(x, y):
        p = intcode.Process(program)
        p.write_in(x)
        p.write_in(y)
        r = p.read_out()
        assert r in [0, 1]
        return r == 1

        #for i in range(len(beam)):
        #    for j in range(len(beam[i])):
        #        if (i, j) == (x, y):
        #            if beam[i][j] == '.':
        #                print('%', end='')
        #            else:
        #                print('*', end='')
        #        else:
        #            print(beam[i][j], end='')
        #    print()
        #print()

        #return beam[x][y] != '.'


    slopes = set()
    for i in range(1, 50):
        slopes.add(Fraction(i, 50))
        slopes.add(Fraction(50, i))
    slopes = sorted(slopes)

    for a, b in pairwise(slopes):
        if pulled(b.denominator, b.numerator):
            slope_min = a
            break

    for a, b in pairwise(reversed(slopes)):
        if pulled(b.denominator, b.numerator):
            slope_max = a
            break

    # a = y/(x+d)
    # b = (y+d)/x
    # ax + ad = y
    # bx = y + d
    # ax + ad = bx - d
    # (b-a)x = (a + 1)d
    # x = (a+1)d/(b-a)

    x = int(math.floor((slope_min + 1) * d / (slope_max - slope_min)))
    y = int(math.floor(slope_min * (x + d)))

    while not (pulled(x + d, y) and pulled(x, y + d)):
        print('.', end='', file=sys.stderr)
        while not pulled(x + d, y):
            y += 1
        while not pulled(x, y + d):
            x += 1

    print(x * 10000 + y)

beam = [
    '#.......................................',
    '.#......................................',
    '..##....................................',
    '...###..................................',
    '....###.................................',
    '.....####...............................',
    '......#####.............................',
    '......######............................',
    '.......#######..........................',
    '........########........................',
    '.........#########......................',
    '..........#########.....................',
    '...........##########...................',
    '...........############.................',
    '............############................',
    '.............#############..............',
    '..............##############............',
    '...............###############..........',
    '................###############.........',
    '................#################.......',
    '.................########OOOOOOOOOO.....',
    '..................#######OOOOOOOOOO#....',
    '...................######OOaOOOOOOO##a..',
    '....................#####OOOOOOOOOO#####',
    '.....................####OOOOOOOOOO#####',
    '.....................####OOOOOOOOOO#####',
    '......................###OOOOOOOOOO#####',
    '.......................##OOOOOOOOOO#####',
    '........................#OOOOOOOOOO#####',
    '.........................OOOOOOOOOO#####',
    '..........................##############',
    '..........................##############',
    '...........................a#########a##',
    '............................############',
    '.............................###########',
]

main()
