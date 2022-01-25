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

    signal = input_digits * REPEATS
    n = len(signal)
    for phase in range(PHASES):
        adder = Adder(signal)
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
                    s += c * adder.block_sum(i, i + block_size - 1)
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

    message = signal[offset:]

    print(''.join(map(str, message)))

class Adder():
    def __init__(self, data):
        self.data = data
        self.aligned_cache = {}

    def block_sum(self, first, last):
        dprint(f"block_sum({first}, {last})")

        first = max(0, first)
        last = min(len(self.data) - 1, last)

        if first == last:
            return self.data[first]

        # Partition into aligned ranges of power-of-two sizes.

        # Structure: A sequence of sub-blocks of increasing size, until the biggest
        # sub-block in the range, then a sequence of decreasing sub-blocks.
        # Either sequence can be empty.
        #
        # Ex: 11-26 (01011-11010)
        #   Sub-blocks: 11 12-15 16-23 24-25 26
        #   Sizes:       1     4     8     2  1
        #
        #   01011
        #       ^ + 1 <= 11010
        #   01100
        #     ^   + 4 <= 11010
        #   10000
        #   ^     + 16 > 11010
        #
        #   01011 remaining
        #   1 ending at 11010: 11010-11010
        #   2 ending at 11001: 11000-11001
        #   8 ending at 10111: 10000-10111

        s = 0
        i = first
        while True:
            # Lowest 1 bit
            b = i & -i
            if b == 0:
                break
            elif i + b <= last:
                s += self.aligned_sum(i, i + b - 1)
                i += b
            else:
                break
        j = last
        while i <= j:
            remaining = j - i + 1
            b = remaining & -remaining
            s += self.aligned_sum(j - b + 1, j)
            j -= b

        return s

    def aligned_sum(self, first, last):
        dprint(f"aligned_sum({first}, {last})")

        if first == last:
            return self.data[first]

        k = (first, last)
        s = self.aligned_cache.get(k)
        if s is None:
            d = last - first + 1
            m = first + d // 2
            s = self.aligned_sum(first, m - 1) + self.aligned_sum(m, last)
            self.aligned_cache[k] = s
        return s

main()

# vim: set shiftwidth=4 tabstop=4 :
