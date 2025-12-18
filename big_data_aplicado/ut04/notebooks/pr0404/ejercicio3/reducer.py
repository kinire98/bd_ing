#!/usr/bin/env python3
import sys

current_country = None
max_variation = 0
max_year = None
buffer = []
for line in sys.stdin:
    country, year, variation = line.strip().split('\t')
    variation = float(variation)
    if country == current_country:
        if variation > max_variation:
            max_variation = variation
            max_year = year
    else:
        if current_country:
            buffer.append(f"{current_country}\t{max_year}")
        current_country = country
        max_variation = variation
        max_year = year
print("\n".join(buffer))
