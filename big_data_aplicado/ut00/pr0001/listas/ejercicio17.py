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
