#!/usr/bin/env python3

import fileinput
import intcode
import multiprocessing as mp
import os
import queue
import sys
from collections import defaultdict
from collections import namedtuple
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")
PROGRESS = os.environ.get("PROGRESS")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

Packet = namedtuple("Packet", "addr x y")

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

    network = mp.Queue()

    n = int(os.environ.get("N", 50))

    nodes = []
    for addr in range(n):
        node = Node(program, addr)
        nodes.append(node)
        node.write_in(addr)

    def run_node(node):
        while True:
            a = node.read_out()
            x = node.read_out()
            y = node.read_out()
            network.put(Packet(a, x, y))

    procs = []
    for node in nodes:
        p = mp.Process(target=run_node, args=(node,), daemon=True)
        procs.append(p)
        p.start()

    while True:
        pkt = network.get()
        dprint(f"Sent: {pkt}")
        if pkt.addr == 255:
            print(pkt.y)
            break

        nodes[pkt.addr].write_packet(pkt)

class Node(intcode.Process):
    def __init__(self, program, addr):
        intcode.Process.__init__(self, program)
        self.addr = addr
        self.queue = mp.Queue()

    def input(self):
        if self._inputs:
            return self._inputs.pop(0)

        try:
            pkt = self.queue.get(timeout=0.001)
            self._inputs.append(pkt.y)
            return pkt.x
        except queue.Empty:
            return -1

    def write_packet(self, pkt):
        self.queue.put(pkt)

main()
