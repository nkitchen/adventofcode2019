#!/usr/bin/env python3

import fileinput
import heapq
import os
import re
import sys
from pprint import pprint
from collections import defaultdict
from collections import namedtuple
from pprint import pprint

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
    def __str__(self):
        keys = sorted(self.collected_keys)
        #return f"<{self.pos}, {keys}>"
        return f"{''.join(self.pos)} {''.join(keys)}"

    def __repr__(self):
        return str(self)

# Approach: Build an adjacency graph of nodes (vaults, keys, and doors)
# with the steps between them as the edge weights.
# Then do breadth-first search on states.
# A state consists of the combination of nodes where each robot is
# and the set of keys collected by all the robots.

map = {}

def main():
    read_map(fileinput.input())

    prune_map()

    keys = {}
    doors = {}
    vaults = []

    for p, c in map.items():
        if c == '@':
            vaults.append(p)
        elif re.match(r'[a-z]', c):
            keys[c] = p
        elif re.match(r'[A-Z]', c):
            doors[c] = p

    for i, p in enumerate(vaults):
        map[p] = str(i)
    vaults = {str(i): p for i, p in enumerate(vaults)}

    # reachable[u][v] == d: Node u is reachable from node v in d steps
    reachable = defaultdict(dict)

    for u, p in list(keys.items()) + list(doors.items()) + list(vaults.items()):
        dist = {u: 0}
        q = [(p, 0)]
        while q:
            p, d = q.pop(0)
            for n in p.neighbors():
                nc = map[n]
                if nc in ['#', '+']:
                    continue
                elif nc == '.':
                    if n not in dist:
                        dist[n] = d + 1
                        q.append((n, d + 1))
                elif nc in keys or nc in doors or nc in vaults:
                    dist[n] = d + 1
                    reachable[u][nc] = 1 + d

    start_pos = tuple(sorted(vaults))
    start = State(start_pos, frozenset())
    visited = set()
    visited.add(start)

    keys_seen = set()

    q = [(0, 0, start)]
    while q:
        d, nk, s = heapq.heappop(q)

        if DEBUG:
            pprint(q, stream=sys.stderr)
        #dprint("Popped:", d, nk, s)

        for i in range(len(s.pos)):
            u = s.pos[i]
            adj = reachable[u]
            for v, vd in adj.items():
                if (v in s.collected_keys or
                    v in doors and v.lower() in s.collected_keys or
                    v in vaults):
                    pos = s.pos[:i] + (v,) + s.pos[i+1:]
                    t = State(pos, s.collected_keys)
                    if t not in visited:
                        visited.add(t)
                        heapq.heappush(q, (d + vd, nk, t))
                elif v in keys and v not in s.collected_keys:
                    #if PROGRESS and c not in keys_seen:
                    #    keys_seen.add(c)
                    #    print('.', end='')
                    pos = s.pos[:i] + (v,) + s.pos[i+1:]
                    t = State(pos, s.collected_keys | frozenset([v]))
                    if len(t.collected_keys) == len(keys):
                        print(d + vd)
                        return

                    if t not in visited:
                        visited.add(t)
                        heapq.heappush(q, (d + vd, -len(t.collected_keys), t))

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
