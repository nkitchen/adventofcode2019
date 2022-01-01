#!/usr/bin/env python3

import fileinput
import os
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    inp = fileinput.input()
    line = next(inp)
    if '-' in line:
        a, b = map(int, line.split('-'))
    else:
        a = int(line)
        b = a

    n = 0
    for p in range(a, b + 1):
        d = digits(p)
        if sorted(d) != d:
            continue
        rle = run_length_encode(d)
        if not any(k == 2 for x, k in rle):
            continue
        n += 1
    print(n)

def digits(p):
    d = []
    while p > 0:
        d.append(p % 10)
        p //= 10
    return list(reversed(d))

def run_length_encode(d):
    r = [[d[0], 1]]
    for i in range(1, len(d)):
        if d[i] == r[-1][0]:
            r[-1][1] += 1
        else:
            r.append([d[i], 1])
    return r

main()
