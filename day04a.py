#!/usr/bin/env python3

import fileinput
import os
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    inp = fileinput.input()
    line = next(inp)
    a, b = map(int, line.split('-'))

    n = 0
    for p in range(a, b + 1):
        d = digits(p)
        if len(set(d)) == len(d):
            continue
        if sorted(d) != d:
            continue
        n += 1
    print(n)

def digits(p):
    d = []
    while p > 0:
        d.append(p % 10)
        p //= 10
    return list(reversed(d))

main()
