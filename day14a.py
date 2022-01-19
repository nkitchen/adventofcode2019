#!/usr/bin/env python3

import fileinput
import functools
from math import ceil
import os
import sys
from collections import Counter
from collections import namedtuple
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def dpprint(x):
    if DEBUG:
        pprint(x, stream=sys.stderr)

class QC(namedtuple('QC', 'quant chem')):
    @staticmethod
    def parse(s):
        n, chem = s.split()
        return QC(int(n), chem)

Reaction = namedtuple('Reaction', 'output inputs')


def main():
    reactions = readReactions()

    # I want to find the total quantity needed of each chemical before comparing to
    # the increments produced.
    # So, I want to work back through products in reverse topological order.

    # Find a topological order.
    topo_index = {'ORE': 0}
    def topo_assign(chem):
        n = topo_index.get(chem)
        if n is not None:
            return

        for inp in reactions[chem].inputs:
            topo_assign(inp.chem)
        topo_index[chem] = len(topo_index)
    topo_assign('FUEL')

    needs = Counter()
    needs['FUEL'] = 1
    for chem, _ in sorted(topo_index.items(), key=lambda item: item[1], reverse=True):
        if chem == 'ORE':
            continue

        r = reactions[chem]
        n = int(ceil(needs[chem] / r.output.quant))
        for inp in r.inputs:
            needs[inp.chem] += n * inp.quant
        dpprint(needs)

    print(needs['ORE'])

# FUEL 1
# > n = 1
# > + (A, 7)
# > > n = 1
# 
# > + (E, 1)

"""
1 FUEL
+- 2 AB
   +- 6 A
   +- 8 B
+- 3 BC
   +- 15 B
   +- 21 C
+- 4 CA
   +- 16 C
   +- 4 A

10 A
+- 45 ORE
23 B
+- 64 ORE
37 C
+- 56 ORE
"""

# 2 AB
# 3 BC
# 4 CA
# 58 C
# 10 A
# 29 B
# 45 ORE A
# 128 ORE B
# 56 ORE C

def readReactions():
    reactions = {}
    for line in fileinput.input():
        lhs, rhs = line.rstrip().split(" => ")
        output = QC.parse(rhs)
        inputs = [QC.parse(s) for s in lhs.split(", ")]
        r = Reaction(output, inputs)
        reactions[r.output.chem] = r

    return reactions

main()
