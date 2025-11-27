#!/usr/bin/env python3

import sys
for line in sys.stdin:
    word, count = line.split(",")
    print(f"{1/int(count)},{word}")
