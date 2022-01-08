#!/usr/bin/env python3

import fileinput
import numpy as np

def main():
    charMap = [list(line.rstrip()) for line in fileinput.input()]
    charMap = np.array(charMap)

    # Asteroid positions
    asteroids = np.argwhere(charMap == '#')

    visible = np.zeros(len(asteroids), dtype=int)

    for i, s in enumerate(asteroids):
        # s = candidate station

        offsets = np.delete(asteroids - s, i, axis=0)

        # Normalizing by the vector length leads to rounding differences.
        # Instead, normalize by the largest component.
        m = np.abs(offsets).max(axis=1, keepdims=True)
        # Signed normalized vector for each offset
        u = offsets / m

        uniq = np.unique(u, axis=0)
        visible[i] = uniq.shape[0]

    print(visible.max())

main()
