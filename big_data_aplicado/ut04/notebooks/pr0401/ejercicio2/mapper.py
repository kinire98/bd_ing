#!/usr/bin/env python3
import sys
chars_to_remove = "\"!·$%&/()=?¿^*¨_:;,.-´`+¡'ºª\|@#~€¬{[]}\¸~ ̣·•• ´´“1234567890\t\n\r\a\b\f\r\t\v\\\n\r–‘‘«»"
with open("palabras.txt") as file:
    content = file.read().split(",")
for line in sys.stdin:
    words = line.split()
    for word in words:
        token = "".join(filter(lambda c: c not in chars_to_remove, word.lower()))
        if token in content:
            continue
        if token:
            print(f"{token}\t1")
