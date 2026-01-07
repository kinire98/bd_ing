#!/usr/bin/env python3
import sys
buffer = []
MAX_LENGTH = 50000
YEAR = 2023

first_names = True
first_gdp = True
def country_code(info, buffer_rec):
    buffer_rec.append(f"{info[2].decode('utf-8')}\t{info[3].decode('utf-8')}")
def country_gdp(info, buffer_rec):
    info = info.split(b";")
    try:
        year = int(info[-4].decode('utf-8'))
        if year != YEAR:
            return
        buffer_rec.append(f"{info[0].decode('utf-8').lower()}\t{info[-3].decode('utf-8')}")
    except IndexError:
        return
for line in sys.stdin.buffer:
    info = line.strip().split(b",") 
    if len(info) == 4:
        if first_names:
            first_names = False
            continue
        country_code(info, buffer)
    else:
        if first_gdp:
            first_gdp = False
            continue
        country_gdp(line, buffer)
    if len(buffer) > 50000:
        "\n".join(buffer)
        buffer = []
if len(buffer) > 0:
    print("\n".join(buffer))
