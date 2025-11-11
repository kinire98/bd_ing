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

