#!/usr/bin/env python3
import sys

current_method = None
current_count = 0
for line in sys.stdin:
    method = line.strip().split(" ")[5]
    method = method.split("\"")[1]
    if method == current_method:
        current_count += 1
    else:
        if current_method:
            print(f"({current_method}\t{current_count})")
        current_method = method
        current_count = 1

if current_method:
    print(f"({current_method}\t{current_count})")
