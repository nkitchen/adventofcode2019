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

def print_char(c):
    print(c, end="")

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    p = intcode.Process(program)
    ready_for_cmd = False
    cmds = [c for c in plan.split('\n') if c]
    location = None
    global items
    items = [i for i in items.split('\n') if i]
    next_item_bits = 1

    def echo_cmd(cmd):
        print(cmd)
        p.write_in_line(cmd)

    while True:
        buf = ""
        while True:
            c = chr(p.read_out())
            buf += c
            if c == "\n":
                print(buf, end="")
                if buf.startswith("== "):
                    location = buf.strip("= \n")
                break
            elif buf.endswith("Command?"):
                print(buf, end="")
                ready_for_cmd = True
                break

        if ready_for_cmd:
            ready_for_cmd = False
            if cmds:
                cmd = cmds.pop(0)
                echo_cmd(cmd)
            elif location == "Security Checkpoint":
                item_bits = next_item_bits
                next_item_bits += 1

                dprint(f"*** Item bits: {item_bits:b}")

                for i in range(len(items)):
                    if (1 << i) & item_bits:
                        cmds.append("take " + items[i])
                    else:
                        cmds.append("drop " + items[i])
                cmds.append("inv")
                cmds.append("south")
                echo_cmd(cmds.pop(0))
            elif not cmds:
                cmd = input()
                p.write_in_line(cmd)
            else:
                break

plan = """
east
south
south
take hologram
north
north
west
south
take mouse
west
take whirled peas
east
east
take shell
west
north
west
north
west
south
take hypercube
north
east
north
west
take semiconductor
east
south
south
west
take antenna
south
take spool of cat6
north
west
south
south
"""

items = """
hologram
mouse
whirled peas
shell
hypercube
semiconductor
antenna
spool of cat6
"""

main()
