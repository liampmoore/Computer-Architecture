#!/usr/bin/env python3

"""Main."""

import sys
import re
from cpu import *


filename = sys.argv[1]

f = open(filename, 'r')

program = []

for line in f:
    bstring = ''
    comment = False
    for c in line:
        if not comment:
            if c == '#':
                comment = True
            elif c == '0' or c == '1':
                bstring = bstring + c
    if len(bstring) == 8:
        program.append(int(bstring, 2))

cpu = CPU()

cpu.load(program)

clock = True

while clock:
    cpu.run()
