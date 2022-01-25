#!/usr/bin/env python3

import fileinput
import itertools
import numpy as np
import os
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
PROGRESS = os.environ.get("PROGRESS")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

REPEATS = int(os.environ.get("REPEATS", 10000))
OFFSET_DIGITS = int(os.environ.get("OFFSET_DIGITS", 7))
PHASES = int(os.environ.get("PHASES", 100))

base_pattern = [0, 1, 0, -1]

def main():
    f = fileinput.input()
    input_line = next(f).rstrip()
    input_digits = [int(c) for c in input_line]

    signal = np.tile(np.array(input_digits), REPEATS)
    n = len(signal)
    for phase in range(PHASES):
        cum = np.cumsum(signal)
        out_signal = np.zeros((n,), dtype=int)
        for out_index in range(n):
            if PROGRESS and out_index % 10000 == 0:
                sys.stderr.write(".")
                sys.stderr.flush()

            block_size = out_index + 1
            pattern_index = 0
            i = -1 # unshift
            s = 0
            while i < n:
                c = base_pattern[pattern_index]
                if c != 0:
                    if block_size == 1:
                        bs = signal[i]
                    else:
                        j = min(n - 1, i + block_size - 1)
                        bs = cum[j] - cum[i - 1]
                    s += c * bs
                i += block_size
                pattern_index = (pattern_index + 1) % len(base_pattern)

            out_signal[out_index] = abs(s) % 10
        if PROGRESS:
            print(file=sys.stderr)

        signal = out_signal

    if OFFSET_DIGITS == 0:
        offset = 0
    else:
        offset = int(input_line[:OFFSET_DIGITS], 10)

    message = signal[offset:offset + 8]

    print(''.join(map(str, message)))

main()

# vim: set shiftwidth=4 tabstop=4 :
