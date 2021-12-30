#!/usr/bin/env python3

import fileinput

def main():
    module_masses = [int(line) for line in fileinput.input()]
    masses = []
    for m in module_masses:
        masses.append(fuel_for(m))
    print(sum(masses))

def fuel_for(m):
    f = []
    while True:
        m = m // 3 - 2
        if m > 0:
            f.append(m)
        else:
            break
    return sum(f)

main()
