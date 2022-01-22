#!/usr/bin/env python3

import fileinput
import os
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)

def main():
    pass

main()
