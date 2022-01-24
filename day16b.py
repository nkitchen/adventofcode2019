#!/usr/bin/env python3

import fileinput
import itertools
import numpy as np
import os
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

REPEATS = int(os.environ.get("REPEATS", 10000))
OFFSET_DIGITS = int(os.environ.get("OFFSET_DIGITS", 7))

base_pattern = [0, 1, 0, -1]

def main():
    f = fileinput.input()
    input_line = next(f).rstrip()
    input_digits = [int(c) for c in input_line]
    n = len(input_digits) * REPEATS

    signal = input_digits
    for phase in range(1):
        adder = Adder(input_digits, REPEATS)
        out_signal = np.zeros((n,), dtype=int)
        for out_index in range(n):
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

        signal = out_signal

    if OFFSET_DIGITS == 0:
        offset = 0
    else:
        offset = int(input_line[:OFFSET_DIGITS], 10)

    message = signal[offset:]

    print(''.join(map(str, message)))

class Adder():
    def __init__(self, data_to_repeat, reps):
        self.data = np.array(data_to_repeat)
        n = len(self.data)

        self.total_length = n * reps

        # self.span_sum[i][j] is the sum of the elements data[i:j+1]
        # (i.e., j is inclusive).
        self.span_sum = np.zeros((n, n), dtype=int)
        for i in range(0, n):
            np.cumsum(self.data[i:], out=self.span_sum[i, i:])

    def block_sum(self, first, last):
        first = max(0, first)
        last = min(self.total_length - 1, last)

        n = len(self.data)

        first_rep = first // n
        first_offset = first % n
        last_rep = last // n
        last_offset = last % n

        if first_rep == last_rep:
            return self.span_sum[first_offset, last_offset]

        s = self.span_sum[first_offset, n - 1]
        s += self.span_sum[0, last_offset]

        middle_reps = last_rep - first_rep - 1
        s += middle_reps * self.span_sum[0, n - 1]

        return s

main()

# vim: set shiftwidth=4 tabstop=4 :
