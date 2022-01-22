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

def main():
    f = fileinput.input()
    input_line = next(f).rstrip()
    input_digits = [int(c) for c in input_line]

    def input_repeated():
        for i in range(REPEATS):
            yield from input_digits

    if OFFSET_DIGITS == 0:
        offset = 0
    else:
        offset = int(input_line[:OFFSET_DIGITS], 10)

    n = len(input_digits)

    base_pattern = [0, 1, 0, -1]

    message_digits = []
    for i in range(offset, offset + 8):
        dprint(f"[{i}]")

        def repeat_pattern():
            while True:
                for b in base_pattern:
                    yield from itertools.repeat(b, i + 1)

        s = 0
        for x, c in zip(itertools.chain.from_iterable([input_digits] * REPEATS),
                        itertools.islice(repeat_pattern(), 1, None)):
            dprint(f"{x} * {c}")
            s += x * c
        dprint(f"= {s}")

        d = abs(s) % 10
        message_digits.append(d)

    print(message_digits)

main()

# vim: set shiftwidth=4 tabstop=4 :
