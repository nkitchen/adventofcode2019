#!/usr/bin/env python3

import sys
import numpy as np

def main():
    line = next(sys.stdin).rstrip()
    data = np.array(list(line), dtype=int)

    if len(sys.argv) > 1:
        w = int(sys.argv[1])
        h = int(sys.argv[2])
    else:
        w = 25
        h = 6

    d = data.size // (w * h)
    img = data.reshape((d, h, w))

    vis = img[0]
    for i in range(1, img.shape[0]):
        vis = np.where(vis == 2, img[i], vis)
    print(vis)

main()
