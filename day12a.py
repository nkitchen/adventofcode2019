#!/usr/bin/env python3

import fileinput
import numpy as np
import re
from pprint import pprint

def main():
    pos = []
    for line in fileinput.input():
        data_only = re.sub(r"[<>xyz=,]", "", line)
        pos.append([int(w) for w in data_only.split()])

    pos = np.array(pos) # (n,d)
    vel = 0 * pos

    for step in range(1000000):
        # Gravity
        lt = pos[:, np.newaxis, :] < pos[np.newaxis, :, :] # (n,1,d) < (1,n,d)
        gt = pos[:, np.newaxis, :] > pos[np.newaxis, :, :] # (n,1,d) < (1,n,d)
        dv = lt.sum(axis=1) - gt.sum(axis=1)
        vel += dv

        # Velocity
        pos += vel

    potential = np.abs(pos).sum(axis=1)
    kinetic = np.abs(vel).sum(axis=1)
    energy = potential * kinetic
    print(energy.sum())

main()
