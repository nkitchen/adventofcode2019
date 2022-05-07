#!/usr/bin/env python3

import fileinput
import os
import re
import sys
from pprint import pprint
from collections import namedtuple
from collections import defaultdict

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

class Point(namedtuple('Point', 'x y')):
    def neighbors(self):
        yield Point(self.x, self.y - 1)
        yield Point(self.x - 1, self.y)
        yield Point(self.x + 1, self.y)
        yield Point(self.x, self.y + 1)

    def opposite_neighbors(self):
        yield (Point(self.x - 1, self.y),
               Point(self.x + 1, self.y))
        yield (Point(self.x, self.y - 1),
               Point(self.x, self.y + 1))

PortalEnd = namedtuple('PortalEnd', 'inside outside')

letters = set(map(chr, range(ord('A'), ord('Z') + 1)))

map = defaultdict(lambda: ' ')
portalByLabel = {}
portalExit = {}
steps = {}

def main():
    read_map(fileinput.input())

    find_portals()

    start = portalByLabel['AA'][0].outside
    goal = portalByLabel['ZZ'][0].outside
    steps[start] = 0
    q = [start]
    while q:
        p = q.pop(0)
        if p == goal:
            print(steps[p])
            return

        for pn in p.neighbors():
            if map[pn] == '.' and pn not in steps:
                steps[pn] = steps[p] + 1
                q.append(pn)
            elif pn in portalExit:
                e = portalExit[pn]
                if e not in steps:
                    steps[e] = steps[p] + 1
                    q.append(e)

def read_map(f):
    global map
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            map[Point(x,y)] = c

def find_portals():
    for p, c in map.items():
        if c not in letters:
            continue

        for pa, pb in p.opposite_neighbors():
            ca = map.get(pa, ' ')
            cb = map.get(pb, ' ')

            if ca == '.' and cb in letters:
                label = c + cb
                end = PortalEnd(p, pa)
                portalByLabel.setdefault(label, []).append(end)
            elif ca in letters and cb == '.':
                label = ca + c
                end = PortalEnd(p, pb)
                portalByLabel.setdefault(label, []).append(end)

    for label in portalByLabel:
        if label in ['AA', 'ZZ']:
            continue
        end1, end2 = portalByLabel[label]
        portalExit[end1.inside] = end2.outside
        portalExit[end2.inside] = end1.outside

main()
