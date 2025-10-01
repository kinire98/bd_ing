lista = [1, 2, 2, 2, 2, 2, 3, 3, 3,35, 5, 5, 4, 4, 25, 35]

frecuencies = dict()

for i in lista:
    frecuencies[i] = frecuencies.get(i, 0) + 1

print(frecuencies)
