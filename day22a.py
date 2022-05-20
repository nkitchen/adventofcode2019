#!/usr/bin/env python3

import fileinput
import os
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

def main():
    n = int(sys.argv[1])

    deck = list(range(n))

    for line in fileinput.input(sys.argv[2:]):
        line = line.rstrip()
        if line == "deal into new stack":
            deck.reverse()
        elif (m := re.match(r"cut (-?\d+)", line)):
            n = int(m.group(1))
            deck = deck[n:] + deck[:n]
        elif (m := re.match(r"deal with increment (\d+)", line)):
            n = int(m.group(1))
            table = deck[:]
            for i, card in enumerate(deck):
                j = (i * n) % len(deck)
                table[j] = card
            deck = table

    i = deck.index(2019)
    print(i)

main()
