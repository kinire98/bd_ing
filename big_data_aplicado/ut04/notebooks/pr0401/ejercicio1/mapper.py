#!/usr/bin/env python3
import sys
chars_to_remove = "\"!·$%&/()=?¿^*¨_:;,.-´`+¡'ºª\|@#~€¬{[]}\¸~ ̣·•• ´´“1234567890\t\n\r\a\b\f\r\t\v\\\n\r–‘‘«»"
for line in sys.stdin:
    words = line.split()
    for word in words:
        token = "".join(filter(lambda c: c not in chars_to_remove, word.lower()))
        if token:
            print(f"{token}\t1")
