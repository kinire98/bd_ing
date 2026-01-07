#!/usr/bin/env python3
import sys

current_earnings = None
current_countries = set()
buffer = []
for line in sys.stdin.buffer:
    line = line.strip().split(b"\t")
    if line[0] != current_earnings:
        if current_earnings:
            buffer.append(f"{current_earnings.decode('utf-8')}\t({', '.join(current_countries)})")
        current_earnings = line[0]
        current_countries = set()
    current_countries.add(line[1].decode("utf-8"))
print("\n".join(buffer))
