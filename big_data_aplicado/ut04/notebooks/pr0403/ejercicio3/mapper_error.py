#!/usr/bin/env python3
import sys
buffer = []
BUFFER_LIMIT = 50000

for line in sys.stdin.buffer:
    if len(line) == 0:
        continue
    split = line.strip().split(b' ')
    url = split[6].decode('utf-8')
    result = 1 if int(split[8].decode('utf-8')) >= 400 else 0
    buffer.append(f"({url}\t{result})")
    if len(buffer) >= BUFFER_LIMIT:
        print("\n".join(buffer))
        buffer = []
if len(buffer) > 0:
    print("\n".join(buffer))
