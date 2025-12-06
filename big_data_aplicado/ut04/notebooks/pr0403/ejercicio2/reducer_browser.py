#!/usr/bin/env python3
import sys

current_browser = None
current_count = 0
buffer = []
BUFFER_LIMIT = 50000
for line in sys.stdin.buffer:
    browser, count = line.strip().split(b"\t")
    browser = browser.split(b"(")[1].decode('utf-8')
    count = int(count.split(b")")[0].decode('utf-8'))
    if browser == current_browser:
        current_count += count
    else:
        if current_browser:
            buffer.append(f"({current_browser}\t{current_count})")
            if len(buffer) >= BUFFER_LIMIT:
                print("\n".join(buffer))
                buffer = []
        current_browser = browser
        current_count = 0
buffer.append(f"({current_browser}\t{current_count})")
if len(buffer) > 0:
    print("\n".join(buffer))
    

