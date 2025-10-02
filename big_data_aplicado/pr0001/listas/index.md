# Ejercicios listas
## Ejercicio 16
```python
lista1 = [1,3,4,5,6,7]
lista2 = [2, 4, 5, 7]


final = []

for i in lista1:
    if i in lista2:
        final.append(i)
    
print(final)
```
![](./ejercicio16.py)
## Ejercicio 17
```python
lista = [1 , 23, 423,45, 5,5,23,42,5,54,4,24,42,24,3]

media = sum(lista) / len(lista)

menor = []
mayor = []

for i in lista:
    if i > media:
        mayor.append(i)
    elif i < media:
        menor.append(i)

print("Mayor: ", mayor)
print("Menor: ", menor)
```
## Ejercicio 18
```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

columnas = len(matrix)

filas = len(matrix[0])


for i in range(columnas):
    print("Fila ", i, ": ", sum(matrix[i]))


for i in range(filas):
    acc = 0
    for j in range(columnas):
        acc += matrix[j][i]
    print("Columna ", i, ": ", acc)
```
## Ejercicio 19
```python
lista = [1, 2, 34,45,5, 5,5,5, 5,5,5, 6, 0]

acc = 1

for i in lista:
    acc *= i

print(acc)
```
## Ejercicio 20
```python
lista = [1, 2, 3, 4, 5, 6, 7]

positions = 3

print(lista[positions:] + lista[:positions] if positions < len(lista) and positions > 0 else "Invalid rotations")
```
## Ejercicio 21
```python
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
```
## Ejercicio 22
```python
normal_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

cuadratic_list = [i**2 for i in normal_list]

print(cuadratic_list)
```
## Ejercicio23
```python
lista = [0, 1, 2, 3, 4, 5, 6, 7]
index_to_remove = int(input("Select an index to remove [min:0, max: " + str(len(lista) - 1) + "]: "))

if index_to_remove < len(lista) and index_to_remove > 0:
    print([lista[i] for i in range(len(lista)) if i != index_to_remove])
else:
    print("Index not valid")

# print("List compression: ")

# print("Up to here, new list")
# print("From here, same list")
#
# print("del keyword: ")
# del lista[index_to_remove]
# print(lista)
#
# print("remove method: ")
# lista.remove(lista[index_to_remove])
# print(lista)
#
# print("pop method: ")
# lista.pop(index_to_remove)
# print(lista)
```
## Ejercicio 24
```python
lista1 = [0, 1, 2, 3, 4]
lista2 = [5, 6, 7, 8, 9, 10, 11, 12]

intercalated = []

for i in range(max(len(lista1), len(lista2))):
    if i >= len(lista1):
        intercalated.append(lista2[i])
        continue
    if i >= len(lista2):
        intercalated.append(lista1[i])
        continue
    intercalated.append(lista1[i])
    intercalated.append(lista2[i])

print(intercalated)
```
## Ejercicio 25
```python
print(list(set([1, 2, 2, 2, 2, 2, 3, 3, 3,35, 5, 5, 4, 4, 25, 35])))
```
## Ejercicio 26
```python
lista = [1, 2, 2, 2, 2, 2, 3, 3, 3,35, 5, 5, 4, 4, 25, 35]

frecuencies = dict()

for i in lista:
    frecuencies[i] = frecuencies.get(i, 0) + 1

print(frecuencies)
```
## Ejercicio 28
```python
list_of_numbers = [1, 2, 1234, 234, 43, 456, 4, 3 ,23, 23]

print((sum(list_of_numbers) - min(list_of_numbers) - max(list_of_numbers)) / len(list_of_numbers))
```
## Ejercicio 29
```python
matrix = [[1, 2], [3, 4], [5, 6]]

lista_plana = []

for i in matrix:
    for j in i:
        lista_plana.append(j)

print(lista_plana)
```
## Ejercicio 30
```python
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
```
## Ejercicio 31
```python
lista = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print([lista[i] for i in range(len(lista)) if i & 1 == 0])
```
## Ejercicio 32 
```python
lista = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print([lista[i] for i in range(len(lista)) if i & 1 == 0])
print([lista[i] for i in range(len(lista)) if i & 1 != 0])
```
## Ejercicio 33
```python
lista = [1, 2, 3, 4, 5, 6, 7]

acc = 0

updated = []

for i in lista:
    updated.append(i + acc)
    acc += i

print(updated)
```
## Ejercicio 34
```python
import random

number = int(input("Number of elements in the list: "))

lista = [random.randrange(0, 101) for _ in range(number)]

print(lista)

print("Max: ", max(lista))
print("Min: ", min(lista))

print("Average: ", sum(lista) / len(lista))
```
