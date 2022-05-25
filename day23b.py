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
QueueStatus = namedtuple("QueueStatus", "addr idle")

def main():
    f = fileinput.input()
    program = [int(x) for x in next(f).split(',')]

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
            pkt = Packet(a, x, y)

            dprint(f"Sending {pkt}")
            if pkt.addr == 255:
                nat_queue.put(pkt)
            else:
                nodes[pkt.addr].write_packet(pkt)
                nat_queue.put(QueueStatus(pkt.addr, False))

    procs = []
    for node in nodes:
        p = mp.Process(target=run_node, args=(node,), daemon=True)
        procs.append(p)
        p.start()

    def run_nat():
        last_packet = None
        sent_y = set()
        idlers = set()

        while True:
            try:
                msg = nat_queue.get(timeout=0.010)
                dprint(f"NAT received: {msg}")
                if isinstance(msg, Packet):
                    last_packet = msg
                else:
                    assert isinstance(msg, QueueStatus)
                    if msg.idle:
                        idlers.add(msg.addr)
                    else:
                        idlers.discard(msg.addr)
                    dprint(f"idlers={sorted(idlers)}")
            except queue.Empty:
                if len(idlers) == n:
                    dprint(f"Network is idle.  Sending {last_packet}")
                    nodes[0].write_packet(last_packet)
                    idlers.discard(0)

                    if last_packet.y in sent_y:
                        print(last_packet.y)
                        return
                    sent_y.add(last_packet.y)

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
                self.nat_queue.put(QueueStatus(self.addr, False))
                self.idle = False
            return pkt.x
        except queue.Empty:
            if not self.idle:
                self.nat_queue.put(QueueStatus(self.addr, True))
                self.idle = True
            return -1

    def write_packet(self, pkt):
        self.queue.put(pkt)

main()
