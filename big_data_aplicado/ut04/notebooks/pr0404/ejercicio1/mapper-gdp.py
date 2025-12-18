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
    try:
        year = int(values[6].decode('utf-8'))
        if year < 2000:
            continue
        gdp = float(values[7].decode('utf-8'))
        if gdp <= 0:
            continue
        country = values[4].decode('utf-8')
        buffer.append(f"{country}\t{year}\t{gdp}")

        if len(buffer) > MAX_BUFFER:
            print("\n".join(buffer))
            buffer = []
    except ValueError:
        continue

if len(buffer) > 0:
    print("\n".join(buffer))
