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
PROGRESS = os.environ.get("PROGRESS")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

class Point(namedtuple('Point', 'x y')):
    def neighbors(self):
        yield Point(self.x, self.y - 1)
        yield Point(self.x - 1, self.y)
        yield Point(self.x + 1, self.y)
        yield Point(self.x, self.y + 1)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"({self.x},{self.y})"

class State(namedtuple('State', 'pos collected_keys')):
    pass

map = {}

def main():
    read_map(fileinput.input())

    prune_map()

    keys = set()
    doors = set()
    vaults = []

    for p, c in map.items():
        if c == '@':
            vaults.append(p)
        elif re.match(r'[a-z]', c):
            keys.add(c)
        elif re.match(r'[A-Z]', c):
            doors.add(c)

    start = State(tuple(vaults), frozenset())
    visited = set()
    visited.add(start)

    keys_seen = set()

    q = [(0, 0, start)]
    while q:
        d, nk, s = heapq.heappop(q)

        dprint("Popped:", d, nk, (s.pos, sorted(s.collected_keys)))

        for i in range(len(s.pos)):
            for n in s.pos[i].neighbors():
                c = map[n]
                if c in '#+':
                    continue
                elif (c in '.@' or
                      (c in keys and c in s.collected_keys) or
                      (c in doors and c.lower() in s.collected_keys)):
                    pos = s.pos[:i] + (n,) + s.pos[i+1:]
                    t = State(pos, s.collected_keys)
                    if t not in visited:
                        visited.add(t)
                        heapq.heappush(q, (1 + d, nk, t))
                elif c in keys and c not in s.collected_keys:
                    if PROGRESS and c not in keys_seen:
                        keys_seen.add(c)
                        print('.', end='')

                    pos = s.pos[:i] + (n,) + s.pos[i+1:]
                    t = State(pos, s.collected_keys | frozenset([c]))
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

# 48s
