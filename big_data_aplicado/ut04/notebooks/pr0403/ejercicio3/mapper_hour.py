#!/usr/bin/env python3
import sys
current_hour = None
current_count = 0
buffer = []
BUFFER_LIMIT = 50000

for line in sys.stdin.buffer:
    hour = line.strip().split(b" ")[3].split(b":")[1].decode('utf-8')
    if hour == current_hour:
        current_count += 1
    else:
        if current_hour:
            buffer.append(f"({current_hour}\t{current_count})")
            if len(buffer) >= BUFFER_LIMIT:
                print("\n".join(buffer))
                buffer = []
        current_hour = hour
        current_count = 1
if current_hour:
    buffer.append(f"({current_hour}\t{current_count})")
    print("\n".join(buffer))
