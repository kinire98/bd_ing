#!/usr/bin/env python3
import sys
buffer = []
MAX_BUFFER = 50000 
first = True
for line in sys.stdin.buffer:
    if first:
        first = False
        continue
    values = line.strip().split(b';')
    region = values[1].decode('utf-8')
    gdp = values[-3].decode('utf-8')
    buffer.append(f"{region}\t{gdp}")
    if len(buffer) > MAX_BUFFER:
        print("\n".join(buffer))
if buffer:
    print("\n".join(buffer))
