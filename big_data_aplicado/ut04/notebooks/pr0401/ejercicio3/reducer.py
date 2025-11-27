#!/usr/bin/env python3

import sys
for line in sys.stdin:
    count, word = line.split(",")
    print(f"{word},{int(1/float(count))}")

