#!/usr/bin/env python3

import fileinput
import numpy as np

def main():
    line = next(fileinput.input()).rstrip()
    data = np.array(list(line), dtype=int)

    w = 25
    h = 6
    d = data.size // (w * h)
    img = data.reshape((d, h, w))

    i_least_zeroes = np.count_nonzero(img, axis=(1, 2)).argmax()
    layer = img[i_least_zeroes]
    n1 = (layer == 1).sum()
    n2 = (layer == 2).sum()
    print(n1 * n2)

main()
