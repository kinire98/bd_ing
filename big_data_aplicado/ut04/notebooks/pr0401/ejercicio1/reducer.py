#!/usr/bin/env python3
import sys

cur_word = None
count = 0
for line in sys.stdin:
    word, _ = line.split("\t")
    if cur_word == word:
        count += 1
    else:
        if cur_word:
            print(f"{cur_word},{count}")
        cur_word = word
        count = 1
if cur_word:
    print(f"{cur_word},{count}")
