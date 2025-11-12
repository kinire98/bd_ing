from typing import List, Tuple


number_dict = {"val1": 5, "val2": 6, "val3": 1, "val4": 10}


items = list(number_dict.items())


def quick_sort(items: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    if len(items) <= 1:
        return items
    pivot = items[0]
    left = [el for el in items[1:] if el[1] < pivot[1]]
    right = [el for el in items[1:] if el[1] > pivot[1]]
    return quick_sort(left) + [pivot] + quick_sort(right)


print(quick_sort(items))
