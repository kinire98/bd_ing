#!/usr/bin/env python3
import sys

current_url = None
current_error = 0
current_count = 0

buffer = []
BUFFER_LIMIT = 50000

for line in sys.stdin.buffer:
    url, result = line.strip().split(b'\t')
    url = url.split(b'(')[1].decode('utf-8')
    result = bool(int(result.split(b')')[0].decode('utf-8')))
    if url == current_url:
        current_count += 1
        if not result:
            current_error += 1
    else:
        if current_url:
            buffer.append(f"({current_url}\t{current_error / current_count * 100}%)")
            if len(buffer) > BUFFER_LIMIT:
                print("\n".join(buffer))
                buffer = []
        current_url = url
        current_count = 1
        current_error = 1 if result else 0
if current_url:
    buffer.append(f"({current_url}\t{current_error / current_count * 100}%)")
    print("\n".join(buffer))

