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
    nat_queue = mp.Queue()

    n = int(os.environ.get("N", 50))

    nodes = []
    for addr in range(n):
        node = Node(program, addr, nat_queue)
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

    def dispatch():
        while True:
            pkt = network.get()
            dprint(f"Dispatched: {pkt}")
            if pkt.addr == 255:
                nat_queue.put(pkt)
            else:
                nodes[pkt.addr].write_packet(pkt)

    dispatcher = mp.Process(target=dispatch, daemon=True)
    dispatcher.start()

    def run_nat():
        last_packet = None
        num_idle = 0
        sent_y = set()

        while True:
            msg = nat_queue.get()
            dprint(f"NAT received: {msg}")
            if isinstance(msg, Packet):
                last_packet = msg
            elif msg >= 0:
                num_idle += msg
                dprint(f"NAT {num_idle=}")
                if num_idle == n:
                    import time
                    time.sleep(20)
                    sys.exit(0)
                    if network.qsize() > 0:
                        # Retry
                        nat_queue.put(0)
                    else:
                        dprint(f"Network is idle {network.qsize()}.  Sending {last_packet}")
                        nodes[0].write_packet(last_packet)
                        num_idle = 0

                        if last_packet.y in sent_y:
                            print(last_packet.y)
                            return
                        sent_y.add(last_packet.y)
            elif msg < 0:
                num_idle -= 1
    nat = mp.Process(target=run_nat)
    nat.start()
    nat.join()

class Node(intcode.Process):
    def __init__(self, program, addr, nat_queue):
        intcode.Process.__init__(self, program)
        self.addr = addr
        self.queue = mp.Queue()
        self.nat_queue = nat_queue
        self.idle = False

    def input(self):
        if self._inputs:
            return self._inputs.pop(0)

        try:
            pkt = self.queue.get(timeout=0.001)
            self._inputs.append(pkt.y)
            if self.idle:
                self.nat_queue.put(-1)
                self.idle = False
            return pkt.x
        except queue.Empty:
            if not self.idle:
                self.nat_queue.put(1)
                self.idle = True
            return -1

    def write_packet(self, pkt):
        self.queue.put(pkt)

main()
