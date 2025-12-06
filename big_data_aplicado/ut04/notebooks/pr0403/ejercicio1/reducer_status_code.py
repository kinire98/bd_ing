#!/usr/bin/env python3
import sys

current_code = None
current_count = 0

for line in sys.stdin:
    status, _ = line.strip().split("\t")
    if status == current_code:
        current_count += 1
    else:
        if current_code != None:
            print(f"{current_code}\t{current_count})")
        current_code = status
        current_count = 1

if current_code != None:
    print(f"{current_code}\t{current_count})")
