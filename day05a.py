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
    inputs = [1]

    c = intcode.Computer()
    outputs = c.run(program, inputs)
    for y in outputs:
        print(y)

class Computer():
    ADD = 1
    MUL = 2
    HALT = 99

    def __init__(self, program):
        self.mem = program[:]

    def run(self):
        pos = 0

        if DEBUG:
            print(f"{pos} ", end='')

        while True:
            opcode = self.mem[pos]
            if opcode == self.ADD:
                pa, pb, pc = self.mem[pos + 1:pos + 4]
                r = self.mem[pa] + self.mem[pb]
                self.mem[pc] = r
            elif opcode == self.MUL:
                pa, pb, pc = self.mem[pos + 1:pos + 4]
                r = self.mem[pa] * self.mem[pb]
                self.mem[pc] = r
            elif opcode == self.HALT:
                break
            else:
                raise Exception(f"Unknown opcode: {opcode}")
            pos += 4

            if DEBUG:
                pprint(self.mem)

main()
