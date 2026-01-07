#!/usr/bin/env python3
import sys

SMALL = "SMALL"
MEDIUM = "MEDIUM"
BIG = "BIG"

small_count = 0
medium_count = 0
big_count = 0

for line in sys.stdin.buffer:
    info = line.strip().split(b"\t")
    category = info[0].decode('utf-8')
    if category == SMALL:
        small_count += 1
    elif category == MEDIUM:
        medium_count += 1
    else:
        big_count += 1
print(f"{SMALL}\t{small_count}")
print(f"{MEDIUM}\t{medium_count}")
print(f"{BIG}\t{big_count}")

