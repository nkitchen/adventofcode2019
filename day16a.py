#!/usr/bin/env python3

import fileinput
import itertools
import numpy as np
import os
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

REPEATS = int(os.environ.get("REPEATS", 1))
MESSAGE_LEN = int(os.environ.get("MESSAGE_LEN", 8))

def main():
    f = fileinput.input()
    input_line = next(f).rstrip()

    input_signal = [int(c) for c in input_line] * REPEATS
    n = len(input_signal)

    base_pattern = [0, 1, 0, -1]

    patterns = []
    for i in range(n):
        # base[0], base[0], ..., base[0], base[1], ..., base[1], ..., base[k]
        # { i + 1 times                }  { i + 1             }       { i + 1 }
        rb = itertools.chain(*[itertools.repeat(p, i + 1) for p in base_pattern])
        pat = list(itertools.islice(itertools.cycle(rb), 1, n + 1))
        patterns.append(pat)

    signal = np.array(input_signal, dtype=int)
    patterns = np.array(patterns, dtype=int)

    for phase in range(100):
        signal = np.abs((signal * patterns).sum(axis=1)) % 10

    s = ''.join(map(str, signal))
    print(s[:MESSAGE_LEN])

main()
