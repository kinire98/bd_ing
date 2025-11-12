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
