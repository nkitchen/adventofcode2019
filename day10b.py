#!/usr/bin/env python3

import fileinput
import numpy as np
from pprint import pprint

# I don't trust np.arctan2 to give exactly equal angles for parallel vectors.
# I can sort by decreasing slope instead:
#   x == 0, y > 0
#   x > 0
#   x == 0, y < 0
#   x < 0

Y_AXIS_POS = 4
X_POS = 3
Y_AXIS_NEG = 2
X_NEG = 1

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

    best = visible.argmax()
    station = asteroids[best]

    # Asteroids are vaporized in reverse sorted order of:
    #   category, slope
    # and I can use negative distance to get the closer ones first.
    q = []

    offsets = asteroids - station
    for i in range(len(offsets)):
        if i == best:
            continue

        dx = offsets[i, 1]
        dy = -offsets[i, 0]
        if dx == 0:
            if dy > 0:
                categ = Y_AXIS_POS
            else:
                categ = Y_AXIS_NEG
            slope = 0
        elif dx > 0:
            categ = X_POS
            slope = dy / dx
        else:
            categ = X_NEG
            slope = dy / dx

        nd2 = -dx**2 - dy**2

        q.append((categ, slope, nd2, asteroids[i]))

    q.sort()
    q.reverse()

    order = []
    while q:
        nq = []
        for i in range(len(q)):
            if i > 0 and q[i][:2] == q[i - 1][:2]:
                # Same line
                nq.append(q[i])
            else:
                a = q[i][-1]
                order.append(a)
        q = nq
    assert len(order) == len(offsets) - 1

    x200 = order[199][1]
    y200 = order[199][0]
    print(x200 * 100 + y200)

main()
