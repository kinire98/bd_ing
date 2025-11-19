#!/usr/bin/env python3

import sys
current_count = 0
current_city = None
for line in sys.stdin:
    city, temp = line.strip().split("\t")
    temp = float(temp)
    if city == current_city:
        temp_in_celsius = (temp - 32) / (9/5)
        if temp_in_celsius > 30:
            current_count += 1
    else:
        if current_city:
            print(f"{current_city}\t{current_count}")
        current_city = city
        current_count = 0

if current_city:
    print(f"{current_city}\t{current_count}")
