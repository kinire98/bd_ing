#!/usr/bin/env python3
import sys

buffer = []
current_code = None
current_country = None
current_gdp = None

for line in sys.stdin.buffer:
    info = line.strip().split(b"\t")
    country_code = info[0].decode('utf-8')
    gdp = None
    country = None
    if country_code != current_code:
        if current_code and current_country:
            buffer.append(f"{current_country}\t{current_gdp}")
        current_code = country_code
        current_country = None
        current_gdp = None
    try:
        current_gdp = float(info[1].decode('utf-8'))
    except ValueError:
        current_country = info[1].decode('utf-8')

buffer.append(f"{current_country}\t{current_gdp}")
print("\n".join(buffer))
