lista = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print([lista[i] for i in range(len(lista)) if i & 1 == 0])
print([lista[i] for i in range(len(lista)) if i & 1 != 0])
