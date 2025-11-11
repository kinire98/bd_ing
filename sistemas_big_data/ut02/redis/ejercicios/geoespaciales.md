# Datos geoespaciales

## Ejercicio 1

```python
import redis
POIS = [
    {"id": "poi_001", "name": "Puerta del Sol", "lon": -3.703790, "lat": 40.416775},
    {"id": "poi_002", "name": "Museo del Prado", "lon": -3.692140, "lat": 40.413780},
    {"id": "poi_003", "name": "Parque del Retiro", "lon": -3.684440, "lat": 40.415360},
    {"id": "poi_004", "name": "Palacio Real", "lon": -3.714310, "lat": 40.417910},
    {"id": "poi_005", "name": "Plaza Mayor", "lon": -3.707370, "lat": 40.415380},
    {"id": "poi_006", "name": "Museo Reina Sofía", "lon": -3.694340, "lat": 40.408010},
    {"id": "poi_007", "name": "Museo Thyssen-Bornemisza", "lon": -3.695000, "lat": 40.416100},
    {"id": "poi_008", "name": "Estadio Santiago Bernabéu", "lon": -3.692380, "lat": 40.453050},
    {"id": "poi_009", "name": "Gran Vía (Plaza Callao)", "lon": -3.708000, "lat": 40.420200},
    {"id": "poi_010", "name": "Templo de Debod", "lon": -3.718000, "lat": 40.424300},
    {"id": "poi_011", "name": "Mercado de San Miguel", "lon": -3.709300, "lat": 40.415000},
    {"id": "poi_012", "name": "Catedral de la Almudena", "lon": -3.714200, "lat": 40.416000},
    {"id": "poi_013", "name": "Estación de Atocha", "lon": -3.690500, "lat": 40.406900},
    {"id": "poi_014", "name": "Plaza de Cibeles", "lon": -3.693000, "lat": 40.419200},
    {"id": "poi_015", "name": "Puerta de Alcalá", "lon": -3.688700, "lat": 40.420500},
    {"id": "poi_016", "name": "Plaza de España", "lon": -3.712000, "lat": 40.423900},
    {"id": "poi_017", "name": "CaixaForum Madrid", "lon": -3.693400, "lat": 40.409300},
    {"id": "poi_018", "name": "Plaza de Cascorro (El Rastro)", "lon": -3.706700, "lat": 40.411100},
    {"id": "poi_019", "name": "Matadero Madrid", "lon": -3.703200, "lat": 40.391600},
    {"id": "poi_020", "name": "Estadio Cívitas Metropolitano", "lon": -3.599100, "lat": 40.436300},
]

r = redis.Redis( 
        host="localhost",
        port=6379, 
        db=0,
        decode_responses=True
        )
key = "poi:locations"
info_key = "poi:info"
for poi in POIS:
    r.geoadd(key, (poi["lon"], poi["lat"], poi["id"]))
    r.hset(info_key, poi["id"], poi["name"])

print("Datos cargados")

```

## Ejercicio 2

```python
import redis 
distance = 2000
usuario = {"lat": 40.41677, "lon": -3.70379}

r = redis.Redis( 
        host="localhost",
        port=6379, 
        db=0,
        decode_responses=True
        )

key = "poi:locations"
info_key = "poi:info"
points_in_2_km = r.geosearch(
    name=key,
    longitude=usuario["lon"], latitude=usuario["lat"],
    radius=distance, unit="m",
    sort="ASC"
    )

for poi in points_in_2_km: # pyright: ignore
    result = r.hget(info_key, poi)
    print(result)
```

## Ejercicio 3

```python
import redis
# usuario = {"lat": 42.609486, "lon": -5.579754} # Leon
# usuario = {"lat": 39.470396, "lon": -0.391444} # Valencia
usuario = {"lat": 37.386162, "lon": -5.992243} # Sevilla

r = redis.Redis( 
        host="localhost",
        port=6379, 
        db=0,
        decode_responses=True
        )


key = "poi:locations"
info_key = "poi:info"

radius = 10

while True: # busca en radios mas grandes cada vez
    result = r.geosearch(name=key, latitude=usuario["lat"], longitude=usuario["lon"], radius=radius, unit="km", sort="ASC", count=1) # pyright: ignore
    if(len(result) > 0): # pyright: ignore
        print(r.hget(info_key, result[0])) # pyright: ignore
        break;
    radius *= 2
```


