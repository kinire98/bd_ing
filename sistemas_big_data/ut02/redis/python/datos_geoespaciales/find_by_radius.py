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
