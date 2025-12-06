#!/usr/bin/env python3
import sys

current_ip = None
current_bytes_count = 0
for line in sys.stdin:
    ip, bytes_count = line.strip().split("\t")
    ip = ip.split("(")[1]
    bytes_count = int(bytes_count.split(")")[0])
    if ip == current_ip:
        current_bytes_count += bytes_count
    else:
        if current_ip:
            print(f"({current_ip}\t{current_bytes_count})")
        current_ip = ip
        current_bytes_count = bytes_count
if current_ip:
    print(f"({current_ip}\t{current_bytes_count})")

