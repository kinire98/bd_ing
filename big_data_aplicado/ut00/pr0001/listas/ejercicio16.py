lista1 = [1,3,4,5,6,7]
lista2 = [2, 4, 5, 7]


final = []

for i in lista1:
    if i in lista2:
        final.append(i)
    
print(final)
    
