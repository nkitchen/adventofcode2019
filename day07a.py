#!/usr/bin/env python3

import fileinput
import intcode
import itertools
import os
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
PROGRESS = os.environ.get("PROGRESS")

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    def thruster_signal(phase_seq):
        signal = 0
        for phase in phase_seq:
            p = intcode.Process(program)
            p.write_in(phase)
            p.write_in(signal)
            signal = p.read_out()
        return signal

    m = max(thruster_signal(phase_seq) 
             for phase_seq in itertools.permutations(range(5)))
    print(m)

main()
