#!/usr/bin/env python3

import fileinput
import intcode
import itertools
import multiprocessing as mp
import os
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
PROGRESS = os.environ.get("PROGRESS")

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    p = intcode.Process(program)
    p.write_in(1)
    for y in p.outputs:
        print(y)

main()
