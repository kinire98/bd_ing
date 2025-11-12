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

