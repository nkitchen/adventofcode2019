#!/usr/bin/env python3

import fileinput
import intcode
import os
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
PROGRESS = os.environ.get("PROGRESS")

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]
    inputs = [5]

    p = intcode.Process(program, inputs)
    outputs = p.run()
    for y in outputs:
        print(y)

main()
