#!/usr/bin/env python3
import sys

MEDIUM_THRESHOLD = 10_000
BIG_THRESHOLD = 1_000_000
SMALL = "SMALL"
MEDIUM = "MEDIUM"
BIG = "BIG"
current_country = None
latest_gdp = None
buffer = []
BUFFER_LIMIT = 50000

first = True
for line in sys.stdin.buffer:
    if first:
        first = False
        continue
    info = line.strip().split(b";")
    country = info[0].decode('utf-8')
    if country != current_country:
        if current_country != None:
            if latest_gdp < MEDIUM_THRESHOLD:
                buffer.append(f"{SMALL}\t{1}")
            elif MEDIUM_THRESHOLD < latest_gdp and latest_gdp < BIG_THRESHOLD:
                buffer.append(f"{MEDIUM}\t{1}")
            else:
                buffer.append(f"{BIG}\t{1}")
            if len(buffer) > BUFFER_LIMIT:
                print("\n".join(buffer))
                buffer = []
        current_country = country
    latest_gdp = float(info[-2].decode('utf-8'))

if len(buffer) > 0:
    print("\n".join(buffer))
