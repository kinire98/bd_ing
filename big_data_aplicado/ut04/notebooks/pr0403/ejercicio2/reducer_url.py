#!/usr/bin/env python3
import sys

url_to_count = dict()

for line in sys.stdin:
    url, count = line.strip().split("\t")
    url = url.split("(")[1]
    count = int(count.split(")")[0])
    url_to_count[url] = url_to_count.get(url, 0) + count
sorted_urls = dict(sorted(url_to_count.items(), key=lambda x: 1/x[1]))
print(sorted_urls)
