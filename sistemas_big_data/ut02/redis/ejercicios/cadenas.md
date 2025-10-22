# Ejercicio cadenas
[Descarga del cuaderno de jupyter](../notebooks/cadenas.ipynb)

## `redis-cli`

1. `SET usuario:nombre Iker`
2. `SET usuario:apellido Nieto`
3. `GET usuario:nombre` - `GET usuario:apellido`
4. `SET usuario:email email@ejemplo.com` - `GET usuario:email`
5. `SET usuario:nombre IKER`
6. `SET contador:visitas 0`
7. `INCR contador:visitas`
8. `SET mensaje "Bienvenido a Redis"`
9. `EXPIRE mensaje 60`
10. `DEL usuario:apellido`
11. `DEL usuario:nombre` - `DEL usuario:email` - `DEL usuario:email` - `DEL contador:visitas` - `DEL mensaje`

## Python
```python
import redis
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)
```

### Ejercicio 1


```python
r.set("app:version", "1.0")
```




    True



### Ejercicio 2


```python
r.get("app:version")
```




    '1.0'



### Ejercicio 3


```python
r.set("app:version", "1.1")
```




    True



### Ejercicio 4


```python
r.set("contador:descargas", 0)
```




    True



### Ejercicio 5


```python
r.incrby("contador:descargas", 5)
```




    5



### Ejercicio 6


```python
r.decrby("contador:descargas", 2)
```




    3



### Ejercicio 7


```python
r.set("app:estado", "activo")
```




    True



### Ejercicio 8


```python
r.set("app:estado", "mantenimiento")
```




    True



### Ejercicio 9


```python
r.set("mensaje:bienvenida", "Hola alumno")
```




    True



### Ejercicio 10


```python
r.expire("app:estado", 30)
```

### Ejercicio 11


```python
import time
time.sleep(30)
print(r.get("app:estado"))
```

    None


### Ejercicio 12


```python
result = r.delete("app:version")
if result == 1:
    print("Eliminado con exito")
else:
    print("No existe")
```

    Eliminado con exito

