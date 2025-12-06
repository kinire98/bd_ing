#!/usr/bin/env python3
import sys 
import re
excluded = set([b'NT', b'like', b'lik', b'Gecko)', b'ONEPLUS', b'X', b'Intel', b'OS', b'Mac', b'Android', b'CPU', b'iPhone', b'IPhone', b'Mobile', b'Version'])
regex = re.compile(b'[;(){}0-9]')
buffer = []
BUFFER_LIMIT = 50000
for line in sys.stdin.buffer:
    browsers = line.strip().rsplit(b"\"", 2)[-2]
    for browser in browsers.split():
        browser_name = browser.split(b"/")[0]
        if browser_name in excluded:
            continue
        if regex.search(browser_name):
            continue
        buffer.append(f"({browser_name.decode('utf-8')}\t1)")
        if len(buffer) >= BUFFER_LIMIT:
            print("\n".join(buffer))
            buffer = []
if len(buffer) > 0:
    print("\n".join(buffer))
    
