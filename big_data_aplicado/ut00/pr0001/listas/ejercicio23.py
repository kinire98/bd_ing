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
