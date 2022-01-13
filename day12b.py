#!/usr/bin/env python3

import fileinput
import itertools
import numpy as np
import re
from pprint import pprint

def main():
    pos = []
    for line in fileinput.input():
        data_only = re.sub(r"[<>xyz=,]", "", line)
        pos.append([int(w) for w in data_only.split()])

    pos = np.array(pos) # (n,d)

    c = []
    for i in range(pos.shape[1]):
        c.append(cycle_time(pos[:, i]))
    c = np.array(c)
    print(c)
    print(np.lcm.reduce(c))

def cycle_time(pos):
    vel = 0 * pos
    seen_at = {tuple(pos) + tuple(vel): 0}

    for t in itertools.count(1):
        # Gravity
        lt = pos[:, np.newaxis] < pos[np.newaxis, :] # (n,1) < (1,n)
        gt = pos[:, np.newaxis] > pos[np.newaxis, :] # (n,1) < (1,n)
        dv = lt.sum(axis=1) - gt.sum(axis=1)
        vel += dv

        # Velocity
        pos += vel

        pv = tuple(pos) + tuple(vel)
        s = seen_at.get(pv)
        if s is not None:
            return t - s

main()
