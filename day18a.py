#!/usr/bin/env python3

import fileinput
import heapq
import os
import re
import sys
from pprint import pprint
from collections import namedtuple
from collections import Counter

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

class State(namedtuple('State', 'pos collected_keys')):
    pass

map = {}

def main():
    read_map(fileinput.input())

    prune_map()

    keys = set()
    doors = set()

    for p, c in map.items():
        if c == '@':
            start_pos = p
        elif re.match(r'[a-z]', c):
            keys.add(c)
        elif re.match(r'[A-Z]', c):
            doors.add(c)

    visited = set()
    start = State(start_pos, frozenset())
    visited.add(start)

    q = [(0, 0, start)]
    while q:
        d, nk, s = heapq.heappop(q)

        dprint("Popped:", d, nk, (s.pos, sorted(s.collected_keys)))

        for n in s.pos.neighbors():
            c = map[n]
            if c in '#+':
                continue
            elif (c in '.@' or
                  (c in keys and c in s.collected_keys) or
                  (c in doors and c.lower() in s.collected_keys)):
                t = State(n, s.collected_keys)
                if t not in visited:
                    visited.add(t)
                    heapq.heappush(q, (1 + d, nk, t))
            elif c in keys and c not in s.collected_keys:
                t = State(n, s.collected_keys | frozenset([c]))
                if len(t.collected_keys) == len(keys):
                    print(d + 1)
                    return

                if t not in visited:
                    visited.add(t)
                    heapq.heappush(q, (1 + d, -len(t.collected_keys), t))

    #x_max = max(p.x for p in map)
    #y_max = max(p.y for p in map)
    #for y in range(0, y_max + 1):
    #    for x in range(0, x_max + 1):
    #        print(map[x,y], end='')
    #    print()

def read_map(f):
    global map
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            map[Point(x,y)] = c

def is_wall(p):
    return map[p] in '#+'

def prune_map():
    global map

    def is_dead_end(p):
        return map[p] == '.' and sum(is_wall(n) for n in p.neighbors()) == 3

    q = []
    for p in map:
        if is_dead_end(p):
            q.append(p)

    while q:
        p = q.pop()
        map[p] = '+'
        for n in p.neighbors():
            if is_dead_end(n):
                q.append(n)

main()
