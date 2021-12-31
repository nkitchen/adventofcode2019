#!/usr/bin/env python3

import fileinput
import os
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    program = [int(x) for x in fileinput.input().readline().split(',')]
    program[1] = 12
    program[2] = 2
    c = Computer(program)
    c.run()
    print(c.mem[0])

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
