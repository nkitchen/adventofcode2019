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

view = None

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    view = defaultdict(lambda: '.')
    p = Robot(program)
    p.mem[0] = 2

    main_routine = 'A,A,B,C,B,C,B,C,C,A'
    fn_A = 'R,8,L,4,R,4,R,10,R,8'
    fn_B = 'L,12,L,12,R,8,R,8'
    fn_C = 'R,10,R,4,R,4'

    p.write_str(main_routine)
    p.write_str(fn_A)
    p.write_str(fn_B)
    p.write_str(fn_C)

    if SHOW:
        p.write_str('y')
    else:
        p.write_str('n')

    while True:
        y = p.read_char()
        if isinstance(y, str):
            if SHOW:
                print(y, end='')
        else:
            print(y)
            break

class Robot(intcode.Process):
    def write_str(self, s):
        for c in s:
            self.write(ord(c))
        self.write(ord('\n'))

    def read_char(self):
        y = self.read()
        if y is not None and y < 128:
            return chr(y)
        return y

main()
