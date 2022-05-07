#!/usr/bin/env python3

import fileinput
import os
import re
import sys
from pprint import pprint
from collections import namedtuple
from collections import defaultdict

DEBUG = os.environ.get("DEBUG")

def dprint(obj):
    if DEBUG:
        pprint(obj, stream=sys.stderr)

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

letters = set(map(chr, range(ord('A'), ord('Z') + 1)))

Loc = namedtuple('Loc', 'point level')
LinkExit = namedtuple('LinkExit', 'point level_delta')
LinkEnd = namedtuple('LinkEnd', 'entrance exit')

map = defaultdict(lambda: ' ')
wall_x_min = None
wall_x_max = None
wall_y_min = None
wall_y_max = None

link_by_label = {}
link_exit = {}
steps = {}

def main():
    read_map(fileinput.input())

    find_links()
    dprint({"link_by_label": link_by_label})
    dprint({"link_exit": link_exit})

    start = Loc(link_by_label['AA'][0].exit.point, 0)
    goal = Loc(link_by_label['ZZ'][0].exit.point, 0)
    steps[start] = 0
    q = [start]
    while q:
        loc = q.pop(0)
        dprint({"steps": steps})
        dprint({"popped": loc})

        if loc == goal:
            print(steps[loc])
            return

        p = loc.point
        for n in p.neighbors():
            if map[n] == '.' and (n_loc := Loc(n, loc.level)) not in steps:
                steps[n_loc] = steps[loc] + 1
                q.append(n_loc)
            elif (exit := link_exit.get(n)):
                e_loc = Loc(exit.point, loc.level + exit.level_delta)
                if e_loc.level < 0:
                    continue

                if e_loc not in steps:
                    steps[e_loc] = steps[loc] + 1
                    q.append(e_loc)

def read_map(f):
    global map
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            map[Point(x,y)] = c

    global wall_x_min
    global wall_x_max
    global wall_y_min
    global wall_y_max
    wall_x_min = min(p.x for p in map if map[p] == '#')
    wall_x_max = max(p.x for p in map if map[p] == '#')
    wall_y_min = min(p.y for p in map if map[p] == '#')
    wall_y_max = max(p.y for p in map if map[p] == '#')

def find_links():
    for p, c in map.items():
        if c not in letters:
            continue

        for pa, pb in p.opposite_neighbors():
            ca = map.get(pa, ' ')
            cb = map.get(pb, ' ')

            if ca == '.' and cb in letters:
                label = c + cb
                d = level_delta(pb)
                link_end = LinkEnd(p, LinkExit(pa, d))
                link_by_label.setdefault(label, []).append(link_end)
            elif ca in letters and cb == '.':
                label = ca + c
                d = level_delta(pa)
                link_end = LinkEnd(p, LinkExit(pb, d))
                link_by_label.setdefault(label, []).append(link_end)

    for label in link_by_label:
        if label in ['AA', 'ZZ']:
            continue
        end1, end2 = link_by_label[label]
        link_exit[end1.entrance] = end2.exit
        link_exit[end2.entrance] = end1.exit

def level_delta(p):
    if (wall_x_min <= p.x <= wall_x_max and
        wall_y_min <= p.y <= wall_y_max):
        # Inside the ring => exiting lowers the level number
        return -1
    else:
        return 1

main()
