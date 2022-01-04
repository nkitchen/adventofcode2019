#!/usr/bin/env python3

import fileinput
import functools
import os
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    orbit_center = {}

    f = fileinput.input()
    for line in f:
        center, orbiter = line.rstrip().split(')')
        orbit_center[orbiter] = center

    if DEBUG:
        pprint(orbit_center)

    @functools.lru_cache(maxsize=None)
    def orbits(x):
        if x == 'COM':
            return 0
        c = orbit_center[x]
        return 1 + orbits(c)

    n = 0
    for x in orbit_center:
        n += orbits(x)
    print(n)

main()
