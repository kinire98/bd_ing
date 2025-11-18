#!/usr/bin/env python3
import sys

first = True
for line in sys.stdin:
    if first:
        first = False
        continue
    values = line.strip().split(",")
    print(f"{values[3]}\t{values[-1]}")
