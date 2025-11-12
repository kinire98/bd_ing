lista = [1, 2, 3, 4, 5, 6, 7]

acc = 0

updated = []

for i in lista:
    updated.append(i + acc)
    acc += i

print(updated)
