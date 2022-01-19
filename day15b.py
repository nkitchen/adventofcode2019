#!/usr/bin/env python3

import fileinput
import intcode
import os
import random
import sys
import time
from collections import defaultdict
from collections import namedtuple
from enum import IntEnum
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
PROGRESS = os.environ.get("PROGRESS")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

class Dir(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

EMPTY = '.'
WALL = '#'
DROID = 'D'
TARGET = '+'
UNKNOWN = '?'

HIT = 0
MOVED = 1
OXYGEN = 2

class Point(namedtuple('Point', 'x y')):
    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return str(self)

    def neighbor(self, direction):
        if direction == Dir.NORTH:
            return Point(self.x, self.y + 1)
        elif direction == Dir.SOUTH:
            return Point(self.x, self.y - 1)
        elif direction == Dir.WEST:
            return Point(self.x - 1, self.y)
        elif direction == Dir.EAST:
            return Point(self.x + 1, self.y)
        assert False

class Droid():
    def __init__(self, program):
        self.control = intcode.Process(program)
        self.status = EMPTY
        self.pos = Point(0, 0)

    def move(self, cmd):
        self.control.write(cmd)
        status = self.control.read()
        self.status = status

        p = self.pos.neighbor(cmd)
        if status in [MOVED, OXYGEN]:
            self.pos = p

map = None
droid = None

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    global map
    global droid
    map = defaultdict(lambda: UNKNOWN)
    droid = Droid(program)
    map[droid.pos] = EMPTY

    o2pos = None

    t = 0
    to_explore = [droid.pos.neighbor(cmd) for cmd in Dir]
    while to_explore:
        dprint("To explore:", to_explore)

        p = to_explore.pop()
        if map[p] != UNKNOWN:
            continue

        t += 1
        r = shortest_route(droid.pos, p)
        dprint("Route:", r)
        for cmd in r:
            droid.move(cmd)

        status = droid.status

        if status == HIT:
            p = droid.pos.neighbor(cmd)
            map[p] = WALL
        else:
            if status == MOVED:
                p = droid.pos
                map[p] = EMPTY
            else:
                assert status == OXYGEN
                p = droid.pos
                map[p] = TARGET

            for d in Dir:
                np = p.neighbor(d)
                if map[np] == UNKNOWN:
                    to_explore.append(np)

        #if t % 10 == 0:
        #    display(file=sys.stderr)
        #    time.sleep(0.1)
        if status == OXYGEN:
            o2pos = droid.pos

    fill_minute = {o2pos: 0}
    q = [(o2pos, 0)]
    while q:
        p, t = q.pop(0)
        for d in Dir:
            np = p.neighbor(d)
            if map[np] != WALL and np not in fill_minute:
                fill_minute[np] = t + 1
                q.append((np, t + 1))
        display(file=sys.stderr, filled=fill_minute.keys())
        time.sleep(0.1)

    print(max(fill_minute.values()))


def shortest_route(src, dest):
    pred = {}

    q = [src]
    while q:
        p = q.pop(0)
        if p == dest:
            break
        for cmd in Dir:
            np = p.neighbor(cmd)
            if (np == dest or
                 (map[np] in [EMPTY, TARGET] and np not in pred)):
                pred[np] = (p, cmd)
                q.append(np)

    route = []
    p = dest
    while p != src:
        p, cmd = pred[p]
        route.append(cmd)

    route.reverse()
    return route

import os
def display(file=sys.stdout, filled=None):
    try:
        os.ttyname(1)
        os.system("clear")
    except OSError:
        pass

    xMin = min(p.x for p in map)
    xMax = max(p.x for p in map)
    yMin = min(p.y for p in map)
    yMax = max(p.y for p in map)

    for y in range(yMax, yMin - 1, -1):
        for x in range(xMin, xMax + 1):
            p = Point(x, y)
            if filled and p in filled:
                print('O', end='', file=file)
            elif p == droid.pos:
                print('D', end='', file=file)
            elif p == Point(0, 0):
                print('o', end='', file=file)
            else:
                print(map[p], end='', file=file)
        print(file=file)
    print(file=file)

main()
