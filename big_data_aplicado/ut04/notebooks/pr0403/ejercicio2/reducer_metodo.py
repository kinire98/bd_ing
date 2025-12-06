#!/usr/bin/env python3
import sys

current_method = None
current_count = 0
for line in sys.stdin:
    method, count = line.strip().split("\t")
    method = method.split("(")[1]
    count = int(count.split(")")[0])
    if method == current_method:
        current_count += count
    else:
        if current_method:
            print(f"({current_method}\t{current_count})")
        current_method = method
        current_count = count

if current_method:
    print(f"({current_method}\t{current_count})")
