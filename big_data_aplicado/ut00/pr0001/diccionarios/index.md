# Ejercicios diccionarios
## Ejercicio 16
```python
dic = {
    "val1": 1,
    "val2": 2,
    "val3": 3,
    "val4": 1,
    "val5": 2,
    "val6": 4,
    "val7": 5,
    "val8": "val"
}

print(list(set(dic.values())))
```
## Ejercicio 17
```python
dic = {
        "val1": [1, 2, 3, 4],
        "val2": [2, 3, 4, 5],
        "val3": [5, 6, 7, 8],
        "val5": [10, 11, 12, 13],
        "val6": [1234, 1234, 1234, 1234],
        }

new_dic = {}

for key, val in dic.items():
    for i in val:
        new_dic[i] = key

print(new_dic)
```
## Ejercicio 18
```python
odd = "odd"
even = "even"


dic = {
        odd: [],
        even: [],
        }

for i in range(1, 21, 1):
    if i & 1 == 0:
        dic[even].append(i)
    else:
        dic[odd].append(i)

print(dic)
```
## Ejercicio 19
```python
dic = {"prod1": 10, "prod2": 15, "prod3": 20, "prod4": 25}
print(sum(dic.values()))
```
## Ejercicio 20
```python
words = ["don't", "come", "easy", "to", "me", "how", "can", "i", "find", "a", "way", "to", "make", "you", "see", "I", "love", "you"]

print({i: len(i) for i in words})
```
## Ejercicio 21
```python
dic = {"ab": 1, "aB": 2, "Ab": 3, "AB": 4}


def invert(string: str) -> str:
    stri = ""
    for c in string:
        if c.islower():
            stri += c.upper()
        else:
            stri += c.lower()
    return stri

print({invert(key): value for (key, value) in dic.items()})
```
## Ejercicio 22
```python
words = ["i", "get", "knocked", "down", "but", "i", "get", "up", "again", "you'll", "never", "keep", "me", "down"]

first_letters = {}

for w in words:
    first_letters.setdefault(w[0], []).append(w)

print(first_letters)
```
## Ejercicio 23
```python
number_list = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]

number_dict = dict()

for i in range(len(number_list)):
    number_dict.setdefault(number_list[i], []).append(i)
print(number_dict)
```
## Ejercicio 24
```python
number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

number_dict = dict()

acc = 0

for i in range(len(number_list)):
    acc += number_list[i]
    number_dict[i] = acc

print(number_dict)
```
## Ejercicio 25
```python
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
```
## Ejercicio 26
```python
tuples_list = [("a", 1), ("b", 2), ("a", 1), ("a", 2)]

tuples_dict = dict()

for el in tuples_list:
    tuples_dict[el] = tuples_dict.get(el, 0) + 1
print(tuples_dict)
```
