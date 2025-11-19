#!/usr/bin/env python3

import sys
current_temps = []
current_country = None
for line in sys.stdin:
    country, temp = line.strip().split("\t")
    temp = float(temp)
    if country == current_country:
        current_temps.append(temp)
    else:
        if current_country:
            print(f"{current_country}\t{sum(current_temps) / len(current_temps)}")
        current_country = country
        current_temps = []

if current_country:
    print(f"{current_country}\t{sum(current_temps) / len(current_temps)}")
