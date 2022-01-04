#!/usr/bin/env python3

import collections
import fileinput
import os
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    adj = collections.defaultdict(list)

    f = fileinput.input()
    for line in f:
        center, orbiter = line.rstrip().split(')')
        adj[orbiter].append(center)
        adj[center].append(orbiter)

    dist = {'YOU': 0}
    q = ['YOU']
    while q:
        u = q.pop(0)

        if DEBUG:
            pprint(dist)
            print(f"Next: {u}")
            print()

        for v in adj[u]:
            if v not in dist:
                dist[v] = 1 + dist[u]
                q.append(v)
            if v == 'SAN':
                print(dist[u] - 1)
                return

main()
