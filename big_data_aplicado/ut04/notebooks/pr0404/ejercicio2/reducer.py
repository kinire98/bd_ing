#!/usr/bin/env python3
import sys
cur_region = None
curr_gdp = 0
buffer = []
for line in sys.stdin:
    region, gdp = line.split("\t")
    gdp = float(gdp)
    if cur_region == region:
        curr_gdp += gdp
    else:
        if cur_region:
            buffer.append(f"{cur_region}\t{curr_gdp}")
        cur_region = region
        curr_gdp = gdp
print("\n".join(buffer))

    
