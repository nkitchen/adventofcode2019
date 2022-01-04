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
        queues = [mp.SimpleQueue() for i in range(len(phase_seq) + 1)]
        procs = []
        for i, phase in enumerate(phase_seq):
            in_q = queues[i]
            out_q = queues[i + 1]
            p = intcode.Process(program, input_queue=in_q, output_queue=out_q)
            procs.append(p)
            p.write(phase)

        procs[0].write(0)

        loop_outputs = []
        while True:
            signal = procs[-1].read()
            if signal is None:
                break
            loop_outputs.append(signal)
            procs[0].write(signal)

        return loop_outputs[-1]

    m = max(thruster_signal(phase_seq)
             for phase_seq in itertools.permutations(range(5, 10)))
    print(m)

main()
