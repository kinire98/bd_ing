from typing import List

def consecutive(int_list: List[int]) -> bool:
    num = int_list[0]
    for i in range(1, len(int_list), 1):
        if int_list[i] != num + 1:
            return False
        num = int_list[i]
    return True

print(consecutive([1, 2, 4, 5]))
print(consecutive([5, 7, 9]))
