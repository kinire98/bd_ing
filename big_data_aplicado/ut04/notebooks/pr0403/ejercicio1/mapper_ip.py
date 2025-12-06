#!/usr/bin/env python3
import sys

for line in sys.stdin:
    if len(line) == 0:
        continue
    status_code = line.split(" ")
    if len(status_code) < 10:
        continue
    print(f"({status_code[0]}\t{status_code[9]})")
