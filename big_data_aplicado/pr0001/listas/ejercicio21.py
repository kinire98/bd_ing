
from typing import List
import math

def second(number_list: List[int]) -> tuple[int, int]:
    biggest = 0
    second_biggest = 0
    lowest = math.inf
    second_lowest = math.inf
    for i in number_list:
        print(i)
        if i > biggest:
            second_biggest = biggest
            biggest = i
        elif i == biggest:
            second_biggest = biggest
        elif i > second_biggest and i < biggest:
            second_biggest = i
        if i < lowest:
            second_lowest = lowest
            lowest = i
        elif i == lowest:
            second_lowest = lowest 
        elif i < second_lowest and i > lowest:
            second_lowest = i
    return (second_biggest, second_lowest) # pyright: ignore


print(second([7, 6, 5, 4, 3, 2, 1, 1234, 1234,1234,1234123,41234]))

