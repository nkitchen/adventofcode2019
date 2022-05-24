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

    def thruster_signal(phase_seq):
        procs = []
        for phase in phase_seq:
            p = intcode.Process(program)
            procs.append(p)
            p.write_in(phase)

        procs[0].write_in(0)

        loop_outputs = []
        while True:
            for i, p in enumerate(procs):
                signal = p.read_out()
                if signal is not None:
                    q = procs[(i + 1) % len(procs)]
                    q.write_in(signal)
                if i == len(procs) - 1:
                    if signal is None:
                        return loop_outputs[-1]
                    else:
                        loop_outputs.append(signal)

    m = max(thruster_signal(phase_seq)
             for phase_seq in itertools.permutations(range(5, 10)))
    print(m)

main()
