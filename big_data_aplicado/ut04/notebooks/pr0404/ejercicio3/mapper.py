#!/usr/bin/env python3
import sys

first = True
buffer = []
MAX_BUFFER = 50000
for line in sys.stdin.buffer:
    if first:
        first = False
        continue
    values = line.strip().split(b';')
    year = values[6].decode('utf-8')
    country = values[4].decode('utf-8')
    variation = values[-1].decode('utf-8')
    buffer.append(f"{country}\t{year}\t{variation}")
    if len(buffer) > MAX_BUFFER:
        print("\n".join(buffer))
if buffer:
    print("\n".join(buffer))
