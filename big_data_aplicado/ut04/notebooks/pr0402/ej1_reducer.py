#!/usr/bin/env python3

import sys
current_city_max_temp = -10000
current_city = None
for line in sys.stdin:
    city, temp = line.strip().split("\t")
    temp = float(temp)
    if city == current_city:
        if temp > current_city_max_temp:
            current_city_max_temp = temp
    else:
        if current_city:
            print(f"{current_city}\t{current_city_max_temp}")
        current_city = city
        current_city_max_temp = temp
if current_city:
    print(f"{current_city}\t{current_city_max_temp}")

    
