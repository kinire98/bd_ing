import random 
from typing import List

random_list = [random.randint(0, 150) for _ in range(300)]

print("=============================================RANDOM=============================================")
print(random_list)
print("================================================================================================")

def quick_sort(sort_list: List[int])-> List[int]:
    if len(sort_list) == 1:
        return sort_list
    if len(sort_list) == 0:
        return sort_list
    pivot = sort_list[-1]
    del sort_list[-1]
    left = []
    right = []
    for el in sort_list:
        if el >= pivot:
            right.append(el)
        else:
            left.append(el)

    return quick_sort(left) + [pivot] + quick_sort(right)

print()
print()
print()
print()
print()
print()
print("=============================================SORTED=============================================")
print(quick_sort(random_list))
print("================================================================================================")
