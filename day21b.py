#!/usr/bin/env python3

import fileinput
import intcode
import os
import sys
from collections import defaultdict
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")
PROGRESS = os.environ.get("PROGRESS")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

# (!A + !B + !C) D (E + H)
# 0--1---1
# -0-1---1
# --01---1
script = """
NOT A T
NOT B J
OR T J
NOT C T
OR T J
AND D J
NOT E T
AND E T
OR E T
OR H T
AND T J
RUN
"""

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    ctrl = Controller(program)

    for line in script.split('\n'):
        if line.strip() == "":
            continue

        ctrl.write_line(line)

    for c in ctrl.outputs:
        if c > 256:
            print(c)
            break
        print(chr(c), end='')

class Controller(intcode.Process):
    def write_line(self, s):
        for c in s:
            self.write(ord(c))
        self.write(ord('\n'))

main()
