#!/usr/bin/env python3

import fileinput

def main():
    module_masses = [int(line) for line in fileinput.input()]
    fuels = [m // 3 - 2 for m in module_masses]
    print(sum(fuels))

main()
