#Ejercicio 1
import redis
import json

r = redis.Redis(
        host="localhost",
        port=6379, 
        db=0,
        decode_responses=True
        )
counter = 1
key = "pedidos"
# Ejercicio 2
def agregar_pedido(cliente: str, producto: str, pedido: int, urgente: bool):
                # Ejercicio 4
    pedido_json = json.dumps({
        "id": "pedido_00" + str(pedido),
        "cliente": cliente,
        "producto": producto,
        # Ejercicio 3
        "cantidad": 1,
        "urgente": urgente,
        })
    if urgente:
        r.lpush(key, pedido_json)
    else:
        r.rpush(key, pedido_json)
# Ejercicio 5
def procesar_pedido() -> bool:
    if r.llen(key) == 0:
        return False
    json_ = r.lpop(key)
    print(json.loads(json_)) # pyright: ignore
    return True
# Ejercicio 6
nombres_productos = [
        ["Jose Luis", "Maquinilla de afeitar"],
        ["Javier", "Ordenador"],
        ["Maricarmen", "Pegatina"],
        ["Pereza", "Lady Madrid"],
        ["Francisco", "Planta"]
        ]

for i in nombres_productos:
    agregar_pedido(i[0], i[1], counter, False)
    counter += 1
# Ejercicio 7
print(r.lrange(key, 0, -1))
input()
# Ejercicio 8

nombres_productos = [
        ["Ermenegildo", "Silla de ruedas"],
        ["Antonio", "Puros"],
        ]
for i in nombres_productos:
    agregar_pedido(i[0], i[1], counter, False)
    counter += 1
# Ejercicio 9 
while procesar_pedido():
    pass
input()
# Ejercicio 10

nombres_productos = [
        ["Ermenegildo", "Silla de ruedas"],
        ["Antonio", "Puros"],
        ]
for i in nombres_productos:
    agregar_pedido(i[0], i[1], counter, False)
    counter += 1
agregar_pedido("Gobierno", "Top sicret", counter, True)
input()
while procesar_pedido():
    pass
