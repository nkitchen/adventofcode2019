#!/usr/bin/env python3

import fileinput
import os
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
PROGRESS = os.environ.get("PROGRESS")

def main():
    program = [int(x) for x in fileinput.input().readline().split(',')]

    target = 19690720
    for noun in range(0, 100):
        for verb in range(0, 100):
            if PROGRESS:
                print('.', file=sys.stderr, end='')

            program = program[:]
            program[1] = noun
            program[2] = verb

            c = Computer(program)
            try:
                c.run()
            except IndexError:
                pass
            if c.mem[0] == target:
                print(100 * noun + verb)
                return

            if PROGRESS:
                print(file=sys.stderr)

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
