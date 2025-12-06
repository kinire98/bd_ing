#!/usr/bin/env python3
import sys

current_url = None
current_count = 0
for line in sys.stdin:
    if len(line) == 0:
        continue
    info = line.split(" ")
    if len(info) < 7:
        continue
    if current_url == info[6]:
        current_count += 1
    else:
        if current_url:
            print(f"({current_url}\t{current_count})")
        current_url = info[6]
        current_count = 1
if current_url:
    print(f"({current_url}\t{current_count})")
