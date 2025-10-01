lista = [1, 2, 3, 4, 5, 6, 7]

positions = 3

print(lista[positions:] + lista[:positions] if positions < len(lista) and positions > 0 else "Invalid rotations")

