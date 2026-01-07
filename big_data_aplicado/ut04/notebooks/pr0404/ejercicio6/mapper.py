#!/usr/bin/env python3
import sys

EARNINGS_THRESHOLD = 5000
BIG = "BIG EARNINGS"
SMALL = "SMALL EARNINGS"
buffer = []

for line in sys.stdin.buffer:
    line = line.strip()
    if len(line) <= 0:
        continue
    line = line.split(b";")
    if line[0].decode('utf-8') == "country_code":
        continue
    try:
        name = line[4].decode('utf-8')
        group = line[-5].decode('utf-8')
        buffer.append(f"{group}\t{name}") 
    except (ValueError, IndexError):
        continue
if len(buffer) > 0:
    print("\n".join(buffer))
