import random

number = int(input("Number of elements in the list: "))

lista = [random.randrange(0, 101) for _ in range(number)]

print(lista)

print("Max: ", max(lista))
print("Min: ", min(lista))

print("Average: ", sum(lista) / len(lista))
